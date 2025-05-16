from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from typing import List, Union

from database.dao import Database
from database.models import ActivityOut, OrganizationOut, BuildingOut

router = APIRouter()

@router.get('/api/organization/')
async def search_for_organizations_h(
    req: Request, query: str
) -> JSONResponse:
    
    result = await Database.search_for_organizations(query)
    if result: 
        result = [OrganizationOut.model_validate(model).model_dump(exclude_none=True) for model in result]
        
        return result
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        },
        404
    )


@router.get('/api/organization/id/')
async def organization_by_self_id(
    req: Request, org_id: int
) -> JSONResponse:
    model = await Database.get_organization_by_id(org_id)
    if model: 
        model = OrganizationOut.model_validate(model).model_dump(exclude_none=True)
        return model
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        },
        404
    )


@router.get('/api/organization/buildingId/')
async def organizations_by_building_id(
    req: Request, building_id: int
) -> JSONResponse:
    result = await Database.get_organizations_by_bid(building_id)
    
    if result: 
        result = [OrganizationOut.model_validate(model).model_dump(exclude_none=True) for model in result]
        
        return result
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        }, status_code=404
    )
    
@router.get('/api/organization/inRadius/')
async def organizations_in_radius_m(
    req: Request, radius: float, lat: float, lon: float
) -> JSONResponse:
    result = await Database.organizations_within_radius(lat, lon, radius)
    
    if result: 
        result = [OrganizationOut.model_validate(model).model_dump(exclude_none=True) for model in result]
        
        return result
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        }, status_code=404
    )
    
@router.get('/api/buildings/inRadius/')
async def buildings_in_radius_m(
    req: Request, radius: float, lat: float, lon: float
) -> JSONResponse:
    result = await Database.buildings_within_radius(lat, lon, radius)
    
    if result: 
        result = [BuildingOut.model_validate(model).model_dump(exclude_none=True) for model in result]
        
        return result
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        }, status_code=404
    )


@router.get('/api/organization/activity/')
async def organizations_by_activity_label(
    req: Request, label: str, strict: bool = Query(False, description=(
            "By default set to False.\n"
            "If set to True, returns organizations strictly by given label.\n"
            "If not - returns all organizations, which activity is a descendant of or equal to given activity."
        )
    )
) -> JSONResponse:
    
    result = await Database.get_organizations_by_activity(label, strict=strict)
    
    if result: 
        result = [OrganizationOut.model_validate(model).model_dump(exclude_none=True) for model in result]
        
        return result
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        }, status_code=404
    )

