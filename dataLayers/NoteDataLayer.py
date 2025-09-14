from sqlalchemy.orm import Session
from models.NoteModel import Note
from models.UserModel import User

class NoteDataLayer:
    def createNote(self, db: Session, params: dict):
        noteModel = Note(**params)
        db.add(noteModel)
        db.commit()
        db.refresh(noteModel)
        return noteModel
    
    def getNoteById(self, db: Session, note_id: int):
        return db.query(Note).filter(Note.id == note_id).first()

    def getAllNotes(self, db: Session):
        return db.query(Note).all()

    def getNotesByOwnerId(self, db: Session, owner_id: int):
        return db.query(Note).filter(Note.owner_id == owner_id).all()
        
    def updateNote(self, db: Session, note: Note, data: dict):
        for key, value in data.items():
            setattr(note, key, value)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note