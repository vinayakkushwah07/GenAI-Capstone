from data_pipeline.utils import embeddings_transformer
async def get_embeddings(texts:str):
    response =  embeddings_transformer.encode(texts)
    return response