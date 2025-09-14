from fastapi import HTTPException
from requestModels.NoteRequestModels import NoteCreate
from requestModels.AuthRequestModels import Token



class NoteController:
    def crateNote(self,note: NoteCreate):
        if not note.raw_text:
            raise HTTPException(status_code=400, detail="Please enter text")

    def getAllNotes(self,token:Token):
        if not token.is_admin:
            raise HTTPException(
                status_code=403, detail="You do not have permission to access this note"
            )
