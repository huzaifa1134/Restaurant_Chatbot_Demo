import time
from typing import List, Optional
import httpx

BASE_URL = "https://dummyjson.com/recipes"
_CACHE = {"data": None, "ts": 0}
CACHE_TTL = 60

async def _fetch_raw():
  now = time.time()
  if _CACHE["data"] and (now - _CACHE["ts"] < CACHE_TTL):
    return _CACHE["data"]
  
  async with httpx.AsyncClient(timeout=10) as client:
    resp = await client.get(BASE_URL)
    resp.raise_for_status()
    data = resp.json()

  _CACHE["data"] = data
  _CACHE["ts"] = now
  return data

async def get_all(limit: int = 30, skip: int = 0) -> List[dict]:
  data = await _fetch_raw()
  recipes = data.get("recipes", []) if isinstance(data, dict) else []
  normalized = []
  for rec in recipes[skip: skip + limit]:
    name = rec.get("title") or rec.get("name") or rec.get("recipeName") or rec.get("recipe") or ""
    ingredients = rec.get("ingredients") or rec.get("ingredientList") or rec.get("ingredientsList") or []
    normalized.append({
      "id": rec.get("id"),
      "name": name,
      "ingredients": ingredients,
      "raw": rec
    })
  return normalized

async def find_by_name(query: str) -> Optional[dict]:
  q = query.lower().strip()
  recipes = await get_all(limit=100)
  for rec in recipes:
    if rec["name"] and (q == rec["name"].lower() or q in rec["name"].lower()):
      return rec
  return None

async def get_by_id(item_id: int) -> Optional[dict]:
  recipes = await get_all(limit=200)
  for rec in recipes:
    if rec["id"] == item_id:
      return rec
  return None