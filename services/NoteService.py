from sqlalchemy.orm import Session
from dataLayers.NoteDataLayer import NoteDataLayer
from models.UserModel import User
from core.Exceptions import CustomException
from fastapi import HTTPException

class NoteService:
    noteDataLayer = NoteDataLayer()

    def createNote(self, db: Session, raw_text: str, owner: User):
        return self.noteDataLayer.createNote(db, {"raw_text": raw_text, "owner_id": owner.id})

    def getNoteById(self, db: Session, note_id: int, user: User):
        note = self.noteDataLayer.getNoteById(db, note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        # Tenancy Check: Admin değilse ve notun sahibi değilse, erişemez.
        if not user.is_admin and note.owner_id != user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to access this note")
        return note

    def getAllNotes(self, db: Session, user: User):
        # Tenancy Check: Admin ise tüm notları, değilse sadece kendi notlarını görür.
        if user.is_admin:
            return self.noteDataLayer.getAllNotes(db)
        return self.noteDataLayer.getNotesByOwnerId(db, owner_id=user.id)