import os
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import List


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True,
#     future=True,
#     pool_size=5,
# )

engine = create_engine(DATABASE_URL)

# async def init_db():
#     async with engine.begin() as conn:
#         # await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/")
def defaultHanlder():
    return {"hello": "world"}

@app.post("/items/", response_model=Hero)
def create_item(item: Hero, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/items/", response_model=List[Hero])
def read_items(session: Session = Depends(get_session)):
    items = session.exec(select(Hero)).all()
    return items

# @app.post("/heroes/")
# def create_hero(hero: Hero):
#     # with Session(engine) as session:
#     with SessionLocal.begin() as session:
#         session.add(hero)
#         session.commit()
#         session.refresh(hero)
#         return hero


# @app.get("/heroes/")
# def read_heroes():
#     with SessionLocal.begin() as session:
#         heroes = session.exec(select(Hero)).all()
#         return heroes