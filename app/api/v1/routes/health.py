from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import text 
from app.db.session import get_db


router = APIRouter()

@router.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() != 1:
            raise HTTPException(status_code=503, detail="unexpected result from database")
        return {"status": "connected"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"database unavailable: {e}")
    



