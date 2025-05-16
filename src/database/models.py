from pydantic import BaseModel, ConfigDict, Field, validator
from typing import List, Any, Optional
from sqlalchemy_utils import Ltree
    

class BuildingOut(BaseModel): 
    model_config = ConfigDict(from_attributes=True, exclude_none=True)
    
    id: int
    addr: str
    lat: float
    lon: float
    organizations: Optional[List['OrganizationOut']] = Field(default=None)

class ActivityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, exclude_none=True)
        
    id: int
    label: str
    path: str
    organizations: Optional[List['OrganizationOut']] = Field(default=None)
    
    @validator("path", pre=True)
    def validate_path(cls, value):
        if isinstance(value, Ltree):
            return value.path
        return value

class OrganizationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, exclude_none=True)
        
    id: int
    title: str
    building: BuildingOut
    activities: Optional[List[ActivityOut]] = Field(default=None)
    
OrganizationOut.model_rebuild()
ActivityOut.model_rebuild()
BuildingOut.model_rebuild()