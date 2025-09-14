from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from services.NoteService import NoteService
from services.AISummaryService import AISummaryService
from services.UserService import get_current_user
from models.UserModel import User
from core.Database import get_db
import requestModels.NoteRequestModels as schemas

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    dependencies=[Depends(get_current_user)]
)

note_service = NoteService()
summary_service = AISummaryService()

@router.post("/", response_model=schemas.Note, status_code=202)
def create_note(
    note_data: schemas.NoteCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = note_service.createNote(db, raw_text=note_data.raw_text, owner=current_user)
    background_tasks.add_task(summary_service.process_ai_request, note.id)
    return note

@router.get("/", response_model=List[schemas.Note])
def get_all_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return note_service.getAllNotes(db, user=current_user)

@router.get("/{note_id}", response_model=schemas.Note)
def get_note_by_id(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return note_service.getNoteById(db, note_id=note_id, user=current_user)