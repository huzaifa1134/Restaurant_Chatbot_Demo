from fastapi import APIRouter
from typing import List
from app.models.leads import Lead, Order
from app.services.lead_service import create_lead, get_all_leads, create_order, get_all_orders
from app.services.gemini_service import chat_with_gemini

router = APIRouter(prefix="/crm", tags=["CRM"])

@router.post("/leads", response_model=Lead)
def add_lead(lead: Lead):
  return create_lead(lead)

@router.get("/leads", response_model=List[Lead])
def list_leads():
  return get_all_leads()

@router.post("/orders", response_model=Order)
def add_order(order: Order):
  return create_order(order)

@router.get("/orders", response_model=list[Order])
def list_orders():
  return get_all_orders() 

@router.post("/gemini-chat")
async def chat_with_gemini_route(message: str):
  reply =await chat_with_gemini(message)
  return {"reply": reply}