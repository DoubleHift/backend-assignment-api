from fastapi import FastAPI
from starlette.responses import RedirectResponse

from core.Database import Base, Engine
from routers import auth_router, note_router


#Base.metadata.create_all(bind=Engine)

app = FastAPI(
    title="Backend Candidate Assignment",
    version="1.0.0",
    description="API for a note-taking app with AI summarization."
)

# Router'ları ekle
app.include_router(auth_router.router)
app.include_router(note_router.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')