from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from typing import List

from database.dao import Database
from database.models import ActivityOut, OrganizationOut, BuildingOut
from api.models import QueryPayload

router = FastAPI(
    docs_url="/documentation"
)

@router.get('/api/organization/id/{org_id}')
async def organization_by_id(
    req: Request, org_id: int
) -> JSONResponse:
    model = await Database.get_organization_by_id(org_id)
    if model: 
        model = OrganizationOut.from_orm(model)
        return JSONResponse(
            {
                'status': 'ok',
                'response': model 
            }
        )
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        },
        404
    )


@router.get('/api/organization/buildingId/{building_id}')
async def organizations_by_bid(
    req: Request, building_id: int
) -> JSONResponse:
    result = await Database.get_organizations_by_bid(building_id)
    
    if result: 
        result = [OrganizationOut.from_orm(model) for model in result]
        
        return JSONResponse(
            {
                'status': 'ok',
                'response': result 
            }
        )
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        }, status_code=404
    )

@router.get('/api/organization/activity/{label}')
async def organizations_by_activity(
    req: Request, label: str, strict: bool = Query(False, description=(
            "By default set to False.\n"
            "If set to True, returns organizations strictly by given label.\n"
            "If not - returns all organizations, which activity is a descendant of or equal to given activity."
        )
    )
) -> JSONResponse:
    
    result = await Database.get_organizations_by_activity(label, strict=strict)
    
    if result: 
        result = [OrganizationOut.from_orm(model) for model in result]
        
        return JSONResponse(
            {
                'status': 'ok',
                'response': result 
            }
        )
    
    return JSONResponse(
        {
            'status': 'failed',
            'message': 'Not Found'
        }, status_code=404
    )

