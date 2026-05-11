import random
import asyncio
import sys
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Fix for relative imports
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import AsyncSessionLocal, NetworkMetrics

def get_random_fluctuation(base_value: float) -> float:
    """
    Generate random fluctuation between ±3% and ±7% of base value.
    Returns new intensity.
    """
    fluctuation_percent = random.uniform(0.03, 0.07)  # 3-7%
    direction = random.choice([1, -1])  # up or down
    change = base_value * fluctuation_percent * direction
    new_value = base_value + change
    # Ensure it doesn't go negative
    return max(new_value, 1e-10)

async def sync_network_intensity():
    """
    Async function to update network intensity metrics with simulated fluctuations.
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(NetworkMetrics))
            metrics = result.scalars().all()
            
            for metric in metrics:
                old_value = metric.co2_per_gas_unit
                new_value = get_random_fluctuation(old_value)
                
                metric.co2_per_gas_unit = new_value
                metric.last_updated = datetime.utcnow()
                
                print(f"Updating metrics for {metric.network_name}... Old: {old_value:.10f} | New: {new_value:.10f}")
            
            await session.commit()
        return True
    except Exception as e:
        print(f"Error updating network intensity: {e}")
        return False
