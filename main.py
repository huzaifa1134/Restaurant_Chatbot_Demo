from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings
from app.api.menu import router as menu_router
from app.api.gemini import router as gemini_router


app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)
app.include_router(menu_router)
app.include_router(gemini_router)

@app.get("/")
def root():
    return {"message": "Chatbot demo is running successfully"}