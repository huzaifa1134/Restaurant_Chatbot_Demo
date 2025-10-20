from fastapi import APIRouter, Body
from pydantic import BaseModel
from  app.services.gemini_service import chat_with_gemini
from app.services.menu_service import find_by_name, get_all

router = APIRouter(prefix="/gemini", tags=["gemini"])

class ChatRequest(BaseModel):
  message: str


@router.post("/chat")
async def chat_with_gemini_route(body: ChatRequest = Body(...)):
    
    message = body.message.strip()
    lower = message.lower()
    menu_context = None

    if any(k in lower for k in ["menu", "what is available", "show menu", "available dishes"]):
        menu = await get_all(limit=10)
        menu_context = "\n".join([f"{m['id']}. {m['name']}" for m in menu])
    
    dish = await find_by_name(message) 
    if dish: 
        dish_context = f"{dish['name']}: ingredients -> {', '.join(dish['ingredients']) or 'N/A'}"
        
        if menu_context:
             menu_context += f"\n--\n{dish_context}"
        else:
             menu_context = dish_context
    reply = await chat_with_gemini(message, menu_context)
    return {"reply": reply}