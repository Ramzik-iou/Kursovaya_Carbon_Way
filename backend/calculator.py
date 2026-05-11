from datetime import datetime
from typing import Dict

# CO2 intensity constants (kg CO2 per gas unit)
# These are rough estimates for educational purposes.
INTENSITY = {
    "ETH_POW": 0.0001,      # Pre-merge Ethereum
    "ETH_POS": 0.0000001,   # Post-merge Ethereum
    "POLYGON": 0.00000005,  # Polygon PoS
    "OPTIMISM": 0.00000001, # Optimism L2
}

# Carbon credit price: $30 per ton (1000 kg)
CARBON_PRICE_PER_TON = 30.0

MERGE_TIMESTAMP = datetime(2022, 9, 15).timestamp()

def get_eth_intensity(timestamp: float) -> float:
    """Returns ETH intensity based on whether the transaction was pre or post merge."""
    return INTENSITY["ETH_POW"] if timestamp < MERGE_TIMESTAMP else INTENSITY["ETH_POS"]

def calculate_co2(network: str, gas_used: int, timestamp: float) -> Dict[str, float]:
    """
    Calculates CO2 footprint and potential L2 savings.
    Returns a dict with 'co2' and 'savings_l2'.
    """
    co2 = 0.0
    savings_l2 = 0.0
    
    # Current network footprint
    if network.lower() == "ethereum":
        intensity = get_eth_intensity(timestamp)
        co2 = gas_used * intensity
    elif network.lower() == "polygon":
        co2 = gas_used * INTENSITY["POLYGON"]
        # Savings compared to ETH at that time
        eth_intensity = get_eth_intensity(timestamp)
        savings_l2 = (gas_used * eth_intensity) - co2
    elif network.lower() == "optimism":
        co2 = gas_used * INTENSITY["OPTIMISM"]
        # Savings compared to ETH at that time
        eth_intensity = get_eth_intensity(timestamp)
        savings_l2 = (gas_used * eth_intensity) - co2
        
    return {
        "co2": max(0.0, co2),
        "savings_l2": max(0.0, savings_l2)
    }

def calculate_offset_cost(total_co2_kg: float) -> float:
    """
    Calculates the cost in USD to offset the total CO2 footprint.
    Formula: (total_co2_kg / 1000) * CARBON_PRICE_PER_TON
    """
    return round((total_co2_kg / 1000) * CARBON_PRICE_PER_TON, 2)

def get_analogies(total_co2: float) -> Dict[str, float]:
    """
    Converts kg CO2 into relatable analogies.
    - Kettle: 1 hour of boiling ~ 0.015 kg CO2
    - EV: 1 km in EV ~ 0.05 kg CO2 (depending on energy mix)
    - Tree: 1 tree absorbs ~ 22 kg CO2 per year
    """
    return {
        "kettle_hours": round(total_co2 / 0.015, 2),
        "ev_km": round(total_co2 / 0.05, 2),
        "tree_days": round((total_co2 / 22) * 365, 2)
    }
