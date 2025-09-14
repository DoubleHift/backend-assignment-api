from typing import Optional
from pydantic import BaseModel


class NoteCreate(BaseModel):
    raw_text: str


class Note(BaseModel):
    id: int
    raw_text: str
    summary: Optional[str] = None
    status: str
