from typing import List
from uuid import UUID
from app.models.leads import Lead, Order

leads_db: List[Lead] = []
orders_db: List[Order] = []

def create_lead(lead: Lead) -> Lead:
    leads_db.append(lead)
    return lead 

def get_all_leads() -> List[Lead]:
    return leads_db

def create_order(order: Order) -> Order:
    orders_db.append(order)
    return order

def get_all_orders() -> List[Order]:
    return orders_db