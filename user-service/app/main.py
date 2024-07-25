import os
from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from typing import List
from time import sleep



class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str

class Team(TeamBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="team")

class TeamCreate(TeamBase):
    pass

class TeamPublic(TeamBase):
    id: int

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team: Team | None = Relationship(back_populates="heroes")

class HeroCreate(HeroBase):
    pass

class HeroPublic(HeroBase):
    id: int

class HeroUpdate(SQLModel):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None
    team_id: int | None = None

class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None

class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_HOST = os.getenv("DB_HOST", "localhost")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    print("Creating DB and tables")
    success = False
    while not success:
        try:
            SQLModel.metadata.create_all(engine)
            success = True
        except:
            print("Failed to apply DB migrations")
            sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Setting things up")
    create_db_and_tables()
    print("Finished setting things up")
    yield


app = FastAPI(
    title="EDA-IDM_UserService",
    description="Synchronous API service for CRUD operations against users.",
    version="0.1.0",
    lifespan=lifespan,
)


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

@app.get("/")
def defaultHanlder():
    return {"hello": "world"}


@app.post("/heroes", response_model=HeroPublic)
def create_hero(*, hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes", response_model=List[HeroPublic])
def read_items(*, session: Session = Depends(get_session)):
    items = session.exec(select(Hero)).all()
    return items


@app.get("/heros/{id}", response_model=HeroPublicWithTeam)
def get_hero(*, session: Session = Depends(get_session)):
    hero = session.get(Hero, id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{id}", response_model=HeroPublicWithTeam)
def update_hero(*, hero: Hero, session: Session = Depends(get_session)):
    # Get the hero from the DB - throw 404 if not in DB
    db_hero = session.get(Hero, id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    # Create dict of any attributes from hero sent with request
    # Will only update attributes sent, so not all must be sent
    hero_data = hero.model_dump(exclude_unset=True)
    # Update hero retrieved from DB with values from request
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.delete("/heroes/{id}")
def delete_hero(*, session: Session = Depends(get_session)):
    hero = session.get(Hero, id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"status": "OK"}


@app.post("/teams/", response_model=TeamPublic)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team