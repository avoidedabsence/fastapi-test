from pydantic import BaseModel, validator
from typing import List

class ActivityOut(BaseModel):
    class Config:
        orm_mode = True
        
    id: int
    label: str
    path: List[str]
    organizations: List[OrganizationOut] | None
    
    @validator("path", pre=True)
    def validate_path(cls, value):
        if isinstance(value, str):
            return value.split('.')
        return value
    
class OrganizationOut(BaseModel):
    class Config:
        orm_mode = True
        
    id: int
    title: str
    building: BuildingOut
    activities: List[ActivityOut]

class BuildingOut(BaseModel): 
    class Config:
        orm_mode = True
    
    id: int
    addr: str
    lat: float
    lon: float
    organizations: List[OrganizationOut] | None