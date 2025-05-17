import asyncio
from sqlalchemy import insert, text
from database.dao import Database
from database.orm import Base, BuildORM, OrgORM, ActORM, Relationship_AO
from sqlalchemy_utils import Ltree
from config import Config

async def create_test_data():
    async with Database._engine.begin() as conn:
        
        await conn.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS ltree;"
            )
        )
        
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async with Database._sessionmaker() as session:
        builds = [
            BuildORM(addr=f"ул. Пушкина, дом {i}", lat=55.0 + i, lon=37.0 + i)
            for i in range(1, 6)
        ]
        session.add_all(builds)
        await session.flush()
        
        activities = [
            ActORM(label="Образование", path=Ltree("1")),
            ActORM(label="Среднее образование", path=Ltree("1.1")),
            ActORM(label="Высшее образование", path=Ltree("1.2")),
            ActORM(label="Медицина", path=Ltree("2")),
            ActORM(label="Поликлиника", path=Ltree("2.1")),
            ActORM(label="Больница", path=Ltree("2.2")),
        ]
        session.add_all(activities)
        await session.flush()

        orgs = []
        for i in range(10):
            org = OrgORM(
                title=f"Организация #{i+1}",
                b_id=builds[i % len(builds)].id,
                phone=['2-222-222', '3-333-333', '8-923-666-13-13']
            )
            orgs.append(org)
        session.add_all(orgs)
        await session.flush()

        rels = []
        for i, org in enumerate(orgs):
            rels.append(Relationship_AO(
                org_id=org.id,
                act_id=activities[i % len(activities)].id
            ))
            rels.append(Relationship_AO(
                org_id=org.id,
                act_id=activities[(i + 1) % len(activities)].id
            ))
        session.add_all(rels)

        await session.commit()