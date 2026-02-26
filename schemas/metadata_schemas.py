from typing import Dict, List, Literal, Optional
from pydantic import BaseModel

from schemas.access_role import AccesRole


class MetaData(BaseModel):
    document_id:str
    filename:str
    page_number:int
    section_title:str
    chunk_index:str
    uploaded_by:int
    access_role:Optional[List[AccesRole]]
    ner_data: Dict[str, List[str]]
    
    