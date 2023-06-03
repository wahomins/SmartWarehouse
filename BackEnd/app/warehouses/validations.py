from pydantic import BaseModel
from typing import Optional

class CreateWarehouseModel(BaseModel):
    name: str
    latitude: Optional[str]
    longitude: Optional[str]
    close_land_mark: str
    town: str
    description: Optional[str]
    manager_id: Optional[str]


class UpdateWarehouseModel(BaseModel):
    name: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    close_land_mark: Optional[str]
    town: Optional[str]
    description: Optional[str]
    manager_id: Optional[str]
