from langchain_groq import ChatGroq
from core.settings import settings

try:
    model = ChatGroq(
        model=settings.ADV_MODEL,
        api_key =settings.GROQ_API_KEY,

        temperature=0.1,
        # top_p = 0.7,
        # top_k = 0.8,
        timeout=10,
        max_tokens=5000,
        streaming=True
    )
except Exception as e:
    print(e)    
