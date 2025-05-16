from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from typing import List, Union

from database.dao import Database
from database.models import ActivityOut, OrganizationOut, BuildingOut

router = APIRouter()

@router.get('/api/organization/', summary="Поиск организаций по названию", response_model=List[OrganizationOut], status_code=200)
async def search_for_organizations_h(
    req: Request,
    query: str = Query(..., description="Подстрока для поиска в названии организации")
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


@router.get('/api/organization/id/', summary="Получить организацию по ID", response_model=OrganizationOut, status_code=200)
async def organization_by_self_id(
    req: Request,
    org_id: int = Query(..., description="ID организации")
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


@router.get('/api/organization/buildingId/', summary="Получить организации в здании", response_model=List[OrganizationOut], status_code=200)
async def organizations_by_building_id(
    req: Request,
    building_id: int = Query(..., description="ID здания")
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

@router.get('/api/organization/activity/', summary="Получить организации по деятельности", response_model=List[OrganizationOut], status_code=200)
async def organizations_by_activity_label(
    req: Request,
    label: str = Query(..., description="Название деятельности"),
    strict: bool = Query(
        False,
        description=(
            "Если True — ищет строго по лейблу.\n\n"
            "Если False — включает потомков или совпадающих по иерархии."
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

    
@router.get('/api/organization/inRadius/', summary="Получить организации в радиусе", response_model=List[OrganizationOut], status_code=200)
async def organizations_in_radius_m(
    req: Request,
    radius: float = Query(..., description="Радиус в метрах"),
    lat: float = Query(..., description="Широта точки"),
    lon: float = Query(..., description="Долгота точки")
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
    
@router.get('/api/buildings/inRadius/', summary="Получить здания в радиусе", response_model=List[BuildingOut], status_code=200)
async def buildings_in_radius_m(
    req: Request,
    radius: float = Query(..., description="Радиус в метрах"),
    lat: float = Query(..., description="Широта точки"),
    lon: float = Query(..., description="Долгота точки")
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
