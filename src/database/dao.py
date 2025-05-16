from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import func, cast
from geoalchemy2 import Geography
from loguru import logger
from typing import List

from database.orm import (
    Base, OrgORM, ActORM, BuildORM
)

class Database:
    _engine = None
    _sessionmaker = None
    
    @classmethod
    async def init(cls, db_url: str, max_conn: int):
        cls._engine = create_async_engine(db_url, echo=False, pool_size=max_conn)
        cls._sessionmaker = async_sessionmaker(cls._engine, expire_on_commit=False)
        async with cls._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(
            "[+] Database engine initialized with max {} connections;", max_conn
        )
        return cls._engine

    @classmethod
    async def close(cls):
        if cls._engine:
            await cls._engine.dispose()
            logger.info("[+] Database engine successfully closed;")
            
    @classmethod
    async def get_organization_by_id(cls, org_id: int) -> OrgORM | None:
        async with cls._sessionmaker() as session:
            stmt = (
                select(OrgORM)
                .where(OrgORM.id == org_id)
                .options(
                    selectinload(OrgORM.activities),
                    joinedload(OrgORM.building)
                )
            )
            
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_organizations_by_bid(cls, building_id: int) -> List[OrgORM] | None:
        async with cls._sessionmaker() as session:
            stmt = (
                select(OrgORM)
                .where(OrgORM.b_id == building_id)
                .options(
                    selectinload(OrgORM.activities),
                    joinedload(OrgORM.building)
                )
            )
            
            result = await session.execute(stmt)
            return result.scalars().all() if result else None
    
    @classmethod
    async def get_organizations_by_activity(cls, label: str, strict: bool = False) -> List[OrgORM] | None:
        async with cls._sessionmaker() as session:
            if strict:
                stmt = (
                    select(OrgORM)
                    .join(OrgORM.activities)
                    .options(
                        selectinload(OrgORM.activities),
                        joinedload(OrgORM.building)
                    )
                    .where(ActORM.label == label)
                )
            else:
                parent_path = (await session.execute(
                    select(ActORM.path)
                    .where(ActORM.label == label)
                )).scalar_one_or_none()
                
                if parent_path is None:
                    return None
                
                allowed_act_ids = (await session.execute(
                    select(ActORM.id)
                    .where(ActORM.path.descendant_of(parent_path))
                )).scalars().all()
                
                stmt = (
                    select(OrgORM)
                    .join(OrgORM.activities)
                    .options(
                        selectinload(OrgORM.activities),
                        joinedload(OrgORM.building)
                    )
                    .where(ActORM.id.in_(allowed_act_ids))
                )
            
            result = await session.execute(stmt)
            return result.scalars().all() if result else None
        
    @classmethod
    async def search_for_organizations(cls, query: str) -> List[OrgORM] | None:
        async with cls._sessionmaker() as session:
            stmt = (
                select(OrgORM)
                .where(
                    OrgORM.title.ilike(f"%{query}%")
                )
                .options(
                    selectinload(OrgORM.activities),
                    joinedload(OrgORM.building)
                )
            )
            
            result = await session.execute(stmt)
            return result.scalars().all() if result else None

    @classmethod
    async def organizations_within_radius(cls, lat: float, lon: float, radius: float) -> List[OrgORM] | None:
        print(lat, lon, radius)
        async with cls._sessionmaker() as session:
            stmt = (
                select(OrgORM)
                .join(BuildORM, BuildORM.id == OrgORM.b_id)
                .options(
                    joinedload(OrgORM.building),
                    selectinload(OrgORM.activities)
                )
                .where(
                    func.ST_DWithin(
                        cast(func.ST_SetSRID(
                            func.ST_MakePoint(BuildORM.lon, BuildORM.lat),
                            4326
                        ), Geography),
                        cast(func.ST_SetSRID(
                            func.ST_MakePoint(lon, lat),
                            4326
                        ), Geography),
                        radius
                    )
                )
                .options(
                    selectinload(OrgORM.activities)
                )
            )
            
            result = await session.execute(stmt)
            
            return result.scalars().all() if result else None
    
    @classmethod
    async def buildings_within_radius(cls, lat: float, lon: float, radius: float) -> List[BuildORM] | None:
        async with cls._sessionmaker() as session:
            stmt = (
                select(BuildORM)
                .where(
                    func.ST_DWithin(
                        cast(func.ST_SetSRID(
                            func.ST_MakePoint(BuildORM.lon, BuildORM.lat),
                            4326
                        ), Geography),
                        cast(func.ST_SetSRID(
                            func.ST_MakePoint(lon, lat),
                            4326
                        ), Geography),
                        radius
                    )
                ).options(
                    selectinload(BuildORM.orgs)
                )
            )
            
            result = await session.execute(stmt)
            
            return result.scalars().all() if result else None
