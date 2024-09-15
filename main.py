from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.utils import ingest_csv, calculate_median
from app.schemas import FilterSchema, MedianResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI sensor data service!"}

@app.post("/ingest")
async def ingest_data(url: str, db: AsyncSession = Depends(get_db)):
    try:
        await ingest_csv(db, url)
        return {"status": "success", "message": "Data ingested"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/median", response_model=MedianResponse)
async def get_median(filter: str = Query(None), db: AsyncSession = Depends(get_db)):
    filters = FilterSchema.parse_raw(filter)
    try:
        result = await calculate_median(db, filters.dict(exclude_none=True))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
