from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional

class Lead(BaseModel):
  id: UUID = uuid4()
  name: str
  email: Optional[EmailStr] = None
  phone: Optional[str] = None
  message: Optional[str] = None
  created_at: datetime = datetime.now()

class Order(BaseModel):
  id: UUID = uuid4()
  customer_name: str
  item: str
  quantity: int
  total_price: float
  created_at: datetime = datetime.now()