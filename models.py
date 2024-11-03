from pydantic import BaseModel, Field
from typing import Dict

class CurrentCapacity(BaseModel):
    bio: int
    glass: int
    plastic: int

class WasteStorage(BaseModel):
    id: str
    max_capacity: Dict[str, int]
    current: CurrentCapacity
    distances: Dict[str, int] = Field(default_factory=dict)

    @property
    def available_capacity(self):
        return {k: v - self.current.model_dump().get(k, 0) for k, v in self.max_capacity.items()}

class Organization(BaseModel):
    id: str
    max_capacity: Dict[str, int]
    current: CurrentCapacity
    distances: Dict[str, int]

class Distance(BaseModel):
    from_id: str
    to_id: str
    distance: int
