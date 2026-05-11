from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional

class WalletStatus(BaseModel):
    address: str
    status: str  # "In Progress" or "Completed"
    progress: Optional[float] = None

class ActivityType(BaseModel):
    co2: float
    transactions: int

class NetworkBreakdown(BaseModel):
    network: str
    co2: float
    transactions: int
    savings_l2: float = 0.0
    activity_types: Optional[Dict[str, ActivityType]] = None

class NetworkMetric(BaseModel):
    id: int
    network_name: str
    consensus_type: str
    co2_per_gas_unit: float
    effective_from: datetime
    last_updated: datetime

class WalletResult(BaseModel):
    address: str
    total_co2: float
    breakdown: List[NetworkBreakdown]
    last_updated: datetime
    analogies: Dict[str, float]
    offset_cost: float
    activity_types: Optional[Dict[str, ActivityType]] = None

class AnalysisRequest(BaseModel):
    address: str = Field(..., pattern="^0x[a-fA-F0-9]{40}$")

class SyncStatus(BaseModel):
    last_synced: datetime
    status: str
