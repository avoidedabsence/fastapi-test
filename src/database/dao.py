from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import func, update, cast, bindparam
from loguru import logger

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
    async def get_organization_by_id(cls: Database, org_id: int) -> OrgORM | None:
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
    async def get_organizations_by_bid(cls: Database, building_id: int) -> List[OrgORM] | None:
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
            return result.fetchall() if result else None
    
    @classmethod
    async def get_organizations_by_activity(cls: Database, label: str, strict: bool = False) -> List[OrgORM] | None:
        async with cls._sessionmaker() as session:
            if strict:
                stmt = (
                    select(OrgORM)
                    .join(OrgORM.activities)
                    .options(
                        selectinload(OrgORM.activities)
                    )
                    .where(ActORM.label == label)
                )
            else:
                parent_path = await session.execute(
                    select(ActORM.path)
                    .where(ActORM.label == label)
                ).scalar_one_or_none()
                
                if parent_path is None:
                    return None
                
                allowed_act_ids = await session.execute(
                    select(ActORM.id)
                    .where(ActORM.path.op("@>")(parent_path))
                ).fetchall()
                
                stmt = (
                    select(OrgORM)
                    .join(OrgORM.activities)
                    .options(
                        selectinload(OrgORM.activities)
                    )
                    .where(ActORM.id.in_(allowed_act_ids))
                )
            
            result = await session.execute(stmt)
            return result.fetchall() if result else None
        
        
        
