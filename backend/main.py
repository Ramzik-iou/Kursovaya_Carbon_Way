import os
import sys
import json
import redis.asyncio as redis
import asyncio
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

# Fix for relative imports when running as script
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import AsyncSessionLocal, WalletCache, NetworkMetrics, init_db
from backend.scanner import BlockscoutScanner
from backend.calculator import get_analogies, calculate_offset_cost
from backend.intensity_updater import sync_network_intensity
from backend.schemas import AnalysisRequest, WalletStatus, WalletResult, NetworkBreakdown, SyncStatus

app = FastAPI(title="Carbon Way API")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis setup
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Variable to store last sync time globally
last_sync_time = datetime.utcnow()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def background_intensity_updater():
    """
    Infinite background task to update network intensity every 24 hours.
    Falls back to hourly on error.
    """
    global last_sync_time
    while True:
        try:
            success = await sync_network_intensity()
            if success:
                last_sync_time = datetime.utcnow()
                # Update last_sync_time in Redis too for quick access
                await redis_client.set("last_sync_time", last_sync_time.isoformat())
                # Wait 24 hours
                await asyncio.sleep(24 * 60 * 60)
            else:
                # Try again in 1 hour if failed
                await asyncio.sleep(60 * 60)
        except Exception as e:
            print(f"Error in background intensity updater: {e}")
            # On any error, wait an hour and try again
            await asyncio.sleep(60 * 60)

@app.on_event("startup")
async def startup():
    await init_db()
    # Start background intensity updater
    asyncio.create_task(background_intensity_updater())

async def run_analysis(address: str):
    """Background task to scan and calculate CO2."""
    try:
        await redis_client.set(f"status:{address}", "In Progress")
        
        scanner = BlockscoutScanner()
        results = await scanner.scan_wallet(address)
        
        # Save to database
        async with AsyncSessionLocal() as session:
            wallet = await session.get(WalletCache, address)
            if not wallet:
                wallet = WalletCache(address=address)
                session.add(wallet)
            
            wallet.total_co2 = results["total_co2"]
            wallet.breakdown_json = results
            wallet.last_updated = datetime.utcnow()
            await session.commit()
            
        await redis_client.set(f"status:{address}", "Completed")
        # Cache results in Redis for 1 hour
        await redis_client.set(f"results:{address}", json.dumps(results), ex=3600)
        
    except Exception as e:
        print(f"Error in background analysis for {address}: {e}")
        await redis_client.set(f"status:{address}", f"Error: {str(e)}")

@app.post("/analyze/{address}", response_model=WalletStatus)
async def analyze_wallet(address: str, background_tasks: BackgroundTasks):
    # Basic validation of address format
    if not address.startswith("0x") or len(address) != 42:
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")
    
    status = await redis_client.get(f"status:{address}")
    if status == "In Progress":
        return WalletStatus(address=address, status="In Progress")
    
    background_tasks.add_task(run_analysis, address)
    return WalletStatus(address=address, status="In Progress")

@app.get("/status/{address}", response_model=WalletStatus)
async def get_status(address: str):
    status = await redis_client.get(f"status:{address}")
    if not status:
        return WalletStatus(address=address, status="Not Started")
    return WalletStatus(address=address, status=status)

@app.get("/results/{address}", response_model=WalletResult)
async def get_results(address: str, db: AsyncSession = Depends(get_db)):
    # Try Redis first
    cached = await redis_client.get(f"results:{address}")
    if cached:
        data = json.loads(cached)
    else:
        # Try DB
        wallet = await db.get(WalletCache, address)
        if not wallet:
            raise HTTPException(status_code=404, detail="Analysis results not found")
        
        data = wallet.breakdown_json
    
    # Calculate analogies and offset cost on the fly
    analogies = get_analogies(data["total_co2"])
    offset_cost = calculate_offset_cost(data["total_co2"])
    
    return WalletResult(
        address=data["address"],
        total_co2=data["total_co2"],
        breakdown=[NetworkBreakdown(**b) for b in data["breakdown"]],
        last_updated=datetime.fromisoformat(data["last_updated"]),
        analogies=analogies,
        offset_cost=offset_cost,
        activity_types=data.get("activity_types")
    )

@app.get("/sync-status", response_model=SyncStatus)
async def get_sync_status(db: AsyncSession = Depends(get_db)):
    """
    Get the latest sync status of energy mix data.
    """
    # Try Redis first
    redis_sync = await redis_client.get("last_sync_time")
    if redis_sync:
        last_synced = datetime.fromisoformat(redis_sync)
    else:
        # Fallback to DB: get max last_updated from NetworkMetrics
        result = await db.execute(select(func.max(NetworkMetrics.last_updated)))
        last_synced = result.scalar_one_or_none()
        if not last_synced:
            last_synced = datetime.utcnow()
            
    return SyncStatus(
        last_synced=last_synced,
        status="Live"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
