from langgraph.graph import START, StateGraph, END
from model.context import QAState

from gen_ai.nodes import (
    classify_query,
    complete_query,
    get_rag_data,
    load_memory,
    not_authorized_or_nodata,
    re_get_query,
    refusal,
    response_query,
    route_after_rag,
    route_query,
    save_memory,
    validate_response,
)

workflow = StateGraph(QAState)

workflow.add_node("load_memory", load_memory)
workflow.add_node("classify_query", classify_query)
workflow.add_node("re_get_query", re_get_query)
workflow.add_node("complete_query", complete_query)
workflow.add_node("get_rag_data", get_rag_data)
workflow.add_node("response_query", response_query)
workflow.add_node("refusal", refusal)
workflow.add_node("not_authorized_or_nodata", not_authorized_or_nodata)
workflow.add_node("validate_response", validate_response)
workflow.add_node("save_memory", save_memory)

workflow.add_edge(START, "load_memory")
workflow.add_edge("load_memory", "classify_query")

workflow.add_edge( "get_rag_data","response_query")

workflow.add_edge("re_get_query", "save_memory")
workflow.add_edge("complete_query", "save_memory")
workflow.add_edge("refusal", "save_memory")
workflow.add_edge("validate_response", "save_memory")
workflow.add_edge("not_authorized_or_nodata", "save_memory")
workflow.add_edge("save_memory", END)

workflow.add_conditional_edges(
    "classify_query",
    route_query,
    {
        "re_get_query": "re_get_query",
        "complete_query": "complete_query",
        "refusal": "refusal",
        "get_rag_data": "get_rag_data",
    },
)


workflow.add_conditional_edges(
    "response_query",
    route_after_rag,
    {
        "validate_response": "validate_response",
        "not_authorized_or_nodata": "not_authorized_or_nodata",
    },
)

graph_obj = workflow.compile()
