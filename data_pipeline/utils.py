import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from core.settings import settings

embeddings_transformer = SentenceTransformer(settings.EMBEDDING_MODEL)

chroma_client = chromadb.Client(
    Settings(
        persist_directory=settings.CHROMA_DB_PATH,
        is_persistent=True
    )
)
chroma_collection = chroma_client.get_or_create_collection(
    name=settings.CHROMA_COLLECTION_NAME
)
