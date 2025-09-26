from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()
DB_URL = "sqlite:///./inventory.db"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ItemBase(BaseModel):
    code: str
    name: str

class Item(Base):
    __tablename__ = "machine"
    code = Column(String, primary_key=True, index=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def return_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@app.post("/newEntry")
async def new_entry(entry: ItemBase, db: Session = Depends(get_db)):
    db_item = Item(**entry.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return "OK"

