from data_pipeline.add_to_vdb import filter_rag_data
from gen_ai.core_model import model
from typing import List
from langchain_core.documents import Document
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from llm_guard.input_scanners import PromptInjection

# from typing_extensions import TypedDict
from model.context import QAState

from service.memory_data import get_last_n_messages, save_message_to_db

injection_scanner = PromptInjection(threshold=0.5)

async def summarize_messages(old_messages):

    history_text = "\n".join(f"{m['role']}: {m['content']}" for m in old_messages)

    prompt = f"""
    Summarize the following conversation in a concise way.
    Keep key facts, decisions, and context.

    Conversation:
    {history_text}
    """
    # print("\n\n\n ############################\n from sumarize_msg")
    # print(history_text)
    response = model.invoke(prompt)
    return response.content

async def load_memory(state: QAState) -> QAState:

    messages = await get_last_n_messages(
        db=state.db, user_id=state.user_id, chat_id=state.chat_id, limit=4
    )

    if not messages:
        state.msg_history = []
        return state

    if len(messages) <= 5:
        state.msg_history = messages
        state.chat_summary = None
        return state

    recent = messages[-5:]
    old = messages[:-5]

    state.msg_history = recent
    state.chat_summary = await summarize_messages(old)
    # print("\n\n\n ------------- this is state chat_summary----")
    # print(state.chat_summary )
    return state

async def classify_query(state: QAState) -> QAState:

    history_block = ""

    if state.chat_summary:
        history_block += f"Summary of earlier discussion:\n" f"{state.chat_summary}\n\n"

    if state.msg_history:
        recent_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in state.msg_history
        )
        history_block += f"Recent conversation:\n" f"{recent_text}\n\n"

    prompt = f"""
    You are an Internal Knowledge Assistant.

    Your task is to classify the user's CURRENT question.

    Use the conversation history only to understand context,
    especially for follow-up questions like:
    - "re answer my last question"
    - "explain more"
    - "why?"
    - "what about performance?"

    {history_block}

    Current Question:
    {state.question}

    Classify the CURRENT question into exactly one of:

    - clear → The question is specific and answerable using company documents.
    - ambiguous → The question depends on previous context but is unclear.
    - incomplete → The question is missing important details.
    - out_of_scope → The question is unrelated to company knowledge.

    Respond with ONLY the label.
    """

    response = model.invoke(prompt)
    # print("\n\n\n ############################\n from clasify_query")
    # print(state.msg_history)
    # print("\n this is history block")
    # print(history_block)

    state.query_type = response.content.strip().lower()
    return state

    # response = model.invoke(prompt.format(question=state.question))
    # state.query_type = response.content.strip().lower()
    # return state

async def re_get_query(state: QAState):

    if state.msg_history is None:
        state.msg_history = []

    state.msg_history.append({"role": "user", "content": state.question})

    state.answer = "It looks like an ambiguous question. Please clarify."
    state.final_answer = state.answer

    return state

async def complete_query(state: QAState):

    if state.msg_history is None:
        state.msg_history = []

    state.msg_history.append({"role": "user", "content": state.question})

    state.answer = "It looks like an incomplete question. Please complete it."
    state.final_answer = state.answer

    return state

async def get_rag_data(state: QAState) -> QAState:
    docs = await filter_rag_data(query=state.question, role=state.user_role)

    if not docs and len(state.msg_history) < 1:
        # print("----------------------\n\n\n\n"," the get Rag data is none and setting aswer as null")
        state.documents = []
        state.answer = "null"
        return state

    doc_objects = [
        (
            d
            if isinstance(d, Document)
            else Document(page_content=d, metadata={"role": state.user_role})
        )
        for d in docs
    ]

    # print("-------------------------\n\n docs in get rag data-----")

    state.documents = doc_objects
    return state

async def response_query(state: QAState) -> QAState:

    if not state.documents and len(state.msg_history) < 1:
        state.answer = "null"
        return state

    context = "\n".join([doc.page_content for doc in state.documents])

    history_block = ""

    if state.chat_summary:
        history_block += f"Summary of earlier discussion:\n" f"{state.chat_summary}\n\n"

    if state.msg_history:
        recent_text = "\n".join(
            f"{m['role']}: {m['content']}" for m in state.msg_history
        )
        history_block += f"Recent conversation:\n" f"{recent_text}\n\n"

    prompt = f"""
    You are a conversational assistant.

    {history_block}

    Context:
    {context}

    Current question:
    {state.question}

    Answer in proper markdown format.
    """

    response = model.invoke(prompt)

    state.answer = response.content
    return state

async def refusal(state: QAState) -> QAState:
    state.answer = (
        "I'm sorry, but this question is outside the scope of the available documents."
    )
    return state

async def not_authorized_or_nodata(state: QAState) -> QAState:
    state.answer = "I 'm Sorry , i dont have context regarding this or You are not Authorize to access this data"

async def validate_response(state: QAState) -> QAState:
    if not state.documents:
        state.validation_passed = False
        state.final_answer = state.answer
        return state

    context = "\n".join([doc.page_content for doc in state.documents])

    prompt = f"""
    Validate whether the answer is fully supported by the context.
    If supported, respond: VALID
    If not supported, respond: INVALID
    also provide answer in Md format correctly 

    Context:
    {context}

    Answer:
    {state.answer}
    """

    response = model.invoke(prompt)

    if "VALID" in response.content:
        state.validation_passed = True
        state.final_answer = state.answer
    else:
        state.validation_passed = False
        state.final_answer = (
            "The generated answer could not be validated against the documents."
        )

    return state

async def route_query(state: QAState):
    if state.query_type == "clear":
        return "get_rag_data"

    elif state.query_type == "ambigous":
        return "re_get_query"

    elif state.query_type == "incomplete":
        return "complete_query"

    elif state.query_type == "out_of_scope":
        return "refusal"
    else:
        return "get_rag_data"

async def route_after_rag(state: QAState):
    if state.answer == "null":
        return "not_authorized_or_nodata"
    else:
        return "validate_response"

async def save_memory(state: QAState) -> QAState:

    final_answer = state.final_answer or state.answer

    await save_message_to_db(
        db=state.db,
        user_id=state.user_id,
        chat_id=state.chat_id,
        role="user",
        content=state.question,
    )

    await save_message_to_db(
        db=state.db,
        user_id=state.user_id,
        chat_id=state.chat_id,
        role="assistant",
        content=final_answer,
    )

    return state

async def security_check_node(state: QAState):
    prompt = state.question
    sanitized_prompt, is_safe, risk_score = injection_scanner.scan(prompt)
    if( is_safe < 0.5):
        state.is_safe = False
    else :
        state.is_safe = True
    
async def route_security_check(stae:QAState):
    if(stae.is_safe ):
        return "classify_query"
    else :
        return "refusal"
        
    
