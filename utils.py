import pandas as pd
import requests
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import SensorData

async def ingest_csv(session: AsyncSession, url: str):
    response = requests.get(url)
    df = pd.read_csv(url)
    rows = [
        SensorData(
            id=row['id'],
            type=row['type'],
            subtype=row['subtype'],
            reading=row['reading'],
            location=row['location'],
            timestamp=row['timestamp']
        )
        for _, row in df.iterrows()
    ]
    session.add_all(rows)
    await session.commit()

async def calculate_median(session: AsyncSession, filters: dict):
    query = session.query(SensorData)
    
    # Apply filters if present
    if 'id' in filters:
        query = query.filter(SensorData.id.in_(filters['id']))
    if 'type' in filters:
        query = query.filter(SensorData.type.in_(filters['type']))
    if 'subtype' in filters:
        query = query.filter(SensorData.subtype.in_(filters['subtype']))
    if 'location' in filters:
        query = query.filter(SensorData.location.in_(filters['location']))

    readings = await query.with_entities(SensorData.reading).all()
    readings = [r[0] for r in readings]
    count = len(readings)
    
    if count == 0:
        return {"count": 0, "median": 0}

    readings.sort()
    mid = count // 2

    if count % 2 == 0:
        median = (readings[mid - 1] + readings[mid]) / 2
    else:
        median = readings[mid]

    return {"count": count, "median": median}
