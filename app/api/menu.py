from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.services import menu_service


router = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/", response_model=List[dict])
async def get_menu(limit: int = Query(30, ge=1, le=100), skip: int = 0):
  return await menu_service.get_all(limit=limit, skip=skip)


@router.get("/search")
async def search_menu(name: str):
  item = await menu_service.find_by_name(name)
  return item or []

@router.get("/{item_id}")
async def get_menu_item(item_id: int):
  item = await menu_service.get_by_id(item_id)
  if not item:
    raise HTTPException(status_code=404, detail="Menu Item not Found")
  return item