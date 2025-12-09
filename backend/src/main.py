from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, database

# create tables automatically
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
#create clan
@app.post("/clans/", response_model=schemas.ClanResponse)
def create_clan(clan: schemas.ClanCreate, db: Session = Depends(get_db)):
    db_clan = models.Clan(name=clan.name, region=clan.region)
    db.add(db_clan)
    db.commit()
    db.refresh(db_clan)
    return db_clan

#list clans
@app.get("/clans/", response_model=list[schemas.ClanResponse])
def list_clans(db: Session = Depends(get_db)):
    return db.query(models.Clan).all()

#search clans by name
@app.get("/clans/search", response_model=list[schemas.ClanResponse])
def find_clan(name: str, db: Session = Depends(get_db)):
    if len(name) < 3:
        raise HTTPException(status_code=400, detail="Search must be at least 3 characters")
    # filter by name use contains
    return db.query(models.Clan).filter(models.Clan.name.ilike(f"%{name}%")).all()

@app.delete("/clans/{clan_id}")
def delete_clan(clan_id: str, db: Session = Depends(get_db)):
    clan = db.query(models.Clan).filter(models.Clan.id == clan_id).first()
    if not clan:
        raise HTTPException(status_code=404, detail="Clan not found")
    
    db.delete(clan)
    db.commit()
    return {"detail": "Clan deleted"}