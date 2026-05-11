import os
import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, JSON, DateTime, Float, select
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:45357625@localhost/carbon_way")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class NetworkMetrics(Base):
    __tablename__ = "network_metrics"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    network_name: Mapped[str] = mapped_column(String(50), unique=True)
    consensus_type: Mapped[str] = mapped_column(String(20))  # PoW or PoS
    co2_per_gas_unit: Mapped[float] = mapped_column(Float)
    effective_from: Mapped[datetime] = mapped_column(DateTime)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class WalletCache(Base):
    __tablename__ = "wallet_cache"
    
    address: Mapped[str] = mapped_column(String(64), primary_key=True)
    total_co2: Mapped[float] = mapped_column(Float)
    breakdown_json: Mapped[dict] = mapped_column(JSON)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(NetworkMetrics))
        if not result.scalars().first():
            metrics = [
                NetworkMetrics(
                    network_name="Ethereum_PoW",
                    consensus_type="PoW",
                    co2_per_gas_unit=0.0001, 
                    effective_from=datetime(2015, 7, 30),
                    last_updated=datetime.utcnow()
                ),
                NetworkMetrics(
                    network_name="Ethereum_PoS",
                    consensus_type="PoS",
                    co2_per_gas_unit=0.0000001,
                    effective_from=datetime(2022, 9, 15),
                    last_updated=datetime.utcnow()
                ),
                NetworkMetrics(
                    network_name="Polygon",
                    consensus_type="PoS",
                    co2_per_gas_unit=0.00000005,
                    effective_from=datetime(2020, 5, 31),
                    last_updated=datetime.utcnow()
                ),
                NetworkMetrics(
                    network_name="Optimism",
                    consensus_type="L2",
                    co2_per_gas_unit=0.00000001,
                    effective_from=datetime(2021, 1, 1),
                    last_updated=datetime.utcnow()
                )
            ]
            session.add_all(metrics)
            await session.commit()

if __name__ == "__main__":
    asyncio.run(init_db())
