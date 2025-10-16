from datetime import date
from sqlmodel import SQLModel, Field
from pydantic import ValidationError

class Item(SQLModel):
    name: str = Field(min_length=1)

class EquipmentItem(Item):
    serial: int
    first_operational_date: date
