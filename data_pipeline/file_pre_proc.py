import os
import shutil
from typing import List, Literal, Optional
from fastapi import HTTPException, UploadFile
from core.settings import settings
from data_pipeline.chunk_ner import get_ner_data
from data_pipeline.add_to_vdb import store_chunk
from data_pipeline.chunker import smart_chunk
# from data_pipeline.file_process import chunk_text, clean_text, extract_text_from_pdf
from data_pipeline.cleaner import clean_text
from data_pipeline.ingestion import compute_file_hash, extract_file
from data_pipeline.metadata import detect_section_title
from schemas.access_role import AccesRole
from schemas.metadata_schemas import MetaData


async def upload_file(file: UploadFile , allowed_role:Optional[List[AccesRole]] , uploaded_by):
    print(file.filename)
    if  file.filename.endswith(".pdf"):
       return await upload_pdf(file=file , allowed_role= allowed_role , uploaded_by= uploaded_by)
    else: 
      raise HTTPException(status_code=400, detail="Only PDF files allowed")

async def upload_pdf(file: UploadFile , allowed_role:Optional[List[AccesRole]]  , uploaded_by):
    
    file_path = os.path.join(settings.FILE_PATH, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_bytes = open(file_path, "rb").read()
    doc_id = compute_file_hash(file_bytes)

    pages = extract_file(file_path)

    for page in pages:
        cleaned_text = clean_text(page["text"])
        chunks = smart_chunk(cleaned_text)

        section_title = ""

        for idx, chunk in enumerate(chunks):
            heading = detect_section_title(chunk.split("\n")[0])
            if heading:
                section_title = heading

            chunk_id = f"{doc_id}_p{page['page_number']}_c{idx}"
            meta_data_dict = get_ner_data(chunk)
            metadata = MetaData(
                document_id=doc_id,
                filename= file.filename,
                page_number=page["page_number"],
                section_title= section_title,
                chunk_index=f"'{idx}'",
                ner_data= meta_data_dict,
                access_role=allowed_role,
                uploaded_by=uploaded_by
            )

            await store_chunk(chunk_id, chunk, metadata.model_dump())

    return {"document_id": doc_id, "status": "processed" }


# async def upload_pdf(file: UploadFile):
#     pdf_id = str(uuid.uuid4())
#     pdf_path = os.path.join(settings.FILE_PATH, f"{pdf_id}.pdf")
    
#     async with open(pdf_path, "wb") as f:
#         content = await file.read()
#         await f.write(content)
        
#     text = await extract_text_from_pdf(pdf_path)
#     chunks = await chunk_text(text, 200, 30)

#     embeddings = await get_embeddings(chunks)

#     ids = [f"{pdf_id}_{i}" for i in range(len(chunks))]
    
#     metadata = [{"pdf_id": pdf_id, "chunk_index": i} for i in range(len(chunks))]
#     chroma_collection.add(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadata)
    
#     return {"pdf_id": pdf_id, "chunks_stored": len(chunks)}
