import json
from typing import Dict, List
import faiss
import numpy as np
from core.settings import settings
from data_pipeline.build_embedding import get_embeddings
from data_pipeline.utils import chroma_collection

dimension = 384
index = faiss.IndexFlatL2(dimension)

async def store_chunk(chunk_id, text, my_metadata_obj):
    embedding = await get_embeddings(text)
    index.add(np.array([embedding]).astype("float32"))
    metadata_dict = my_metadata_obj
    final_metadata = {
    "document_id": metadata_dict["document_id"],
    "filename": metadata_dict["filename"],
    "page_number": metadata_dict["page_number"],
    "chunk_index": metadata_dict["chunk_index"],
    "uploaded_by": metadata_dict["uploaded_by"],
    "access_role": [role.value for role in metadata_dict["access_role"]], 
    "ner_data_json": json.dumps(metadata_dict["ner_data"]) 
}

    chroma_collection.add(
        ids= [chunk_id],
        documents=[text],
        embeddings= embedding,
        metadatas= [final_metadata]
    )
    
async def get_rag_data_vdb(query:str , role:str):
    # print(role)
    query_rag_results = chroma_collection.query(
        query_texts=[query],
        n_results=5,
        where={"access_role":{"$contains": role} }
    )
    # print(query_rag_results)
    print("\n\n\n")
    print("--------------this is without role filter---------------")
    # print(chroma_collection.query(query_texts=[query],n_results=1, include=["metadatas", "documents", "distances"]))
    return query_rag_results

async def filter_rag_data(query:str, role:str):
    data = await get_rag_data_vdb(query= query , role= role)
    min_distance = 0.002
    max_distance = 1.5

    filtered_documents = []


    for i in range(len(data["documents"][0])):
        metadata = data["metadatas"][0][i]
        distance = data["distances"][0][i]
        document = data["documents"][0][i]
        
        if (
            role in metadata["access_role"] and
            min_distance <= distance < max_distance
        ):
            filtered_documents.append(document)
            
    return filtered_documents
        

