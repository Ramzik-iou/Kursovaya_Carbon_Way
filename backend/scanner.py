import httpx
import asyncio
import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

# Fix for relative imports
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.calculator import calculate_co2

NETWORKS = {
    "ethereum": "https://eth.blockscout.com/api/v2",
    "polygon": "https://polygon.blockscout.com/api/v2",
    "optimism": "https://explorer.optimism.io/api/v2"
}

# Known DeFi router addresses (sample)
KNOWN_DEFI_ROUTERS = {
    "ethereum": [
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",  # Uniswap V2 Router
        "0xE592427A0AEce92De3Edee1F18E0157C05861564",  # Uniswap V3 Router
    ],
    "polygon": [
        "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678",   # Quickswap Router
    ]
}

# Method signatures
NFT_SIGNATURES = ["mint", "safeMint", "create"]
DEFI_SIGNATURES = ["swap", "multicall", "execute", "addLiquidity", "removeLiquidity"]

def classify_transaction(tx_input: str, to_address: Optional[str] = None, network: str = "ethereum") -> str:
    """
    Classify transaction type: Transfer, NFT, or DeFi.
    """
    tx_input = tx_input.lower() if tx_input else ""
    
    # Check for simple transfer
    if not tx_input or tx_input == "0x":
        return "Transfer"
    
    # Check for NFT activity
    if any(sig.lower() in tx_input for sig in NFT_SIGNATURES) or tx_input.startswith("0x608060"):
        return "NFT"
    
    # Check for DeFi activity
    if any(sig.lower() in tx_input for sig in DEFI_SIGNATURES):
        return "DeFi"
    
    # Check if interacting with known DeFi routers
    if to_address and network in KNOWN_DEFI_ROUTERS:
        if to_address.lower() in [addr.lower() for addr in KNOWN_DEFI_ROUTERS[network]]:
            return "DeFi"
    
    # Default to Transfer if unknown
    return "Transfer"

class BlockscoutScanner:
    def __init__(self):
        self.timeout = httpx.Timeout(30.0)
        
    async def fetch_transactions(self, network_name: str, address: str, next_page_params: Optional[Dict] = None) -> Dict[str, Any]:
        base_url = NETWORKS.get(network_name.lower())
        if not base_url:
            raise ValueError(f"Unsupported network: {network_name}")
            
        url = f"{base_url}/addresses/{address}/transactions"
        params = next_page_params or {}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def scan_wallet(self, address: str) -> Dict[str, Any]:
        total_co2 = 0.0
        total_savings = 0.0
        breakdown = []
        
        # Initialize global activity types counter
        global_activity_types = {
            "DeFi": {"co2": 0.0, "transactions": 0},
            "NFT": {"co2": 0.0, "transactions": 0},
            "Transfer": {"co2": 0.0, "transactions": 0}
        }

        for network_name in NETWORKS.keys():
            network_co2 = 0.0
            network_savings = 0.0
            tx_count = 0
            next_params = None
            
            # Initialize network-specific activity types
            network_activity_types = {
                "DeFi": {"co2": 0.0, "transactions": 0},
                "NFT": {"co2": 0.0, "transactions": 0},
                "Transfer": {"co2": 0.0, "transactions": 0}
            }
            
            pages_scanned = 0
            while pages_scanned < 5:
                try:
                    data = await self.fetch_transactions(network_name, address, next_params)
                    items = data.get("items", [])
                    if not items:
                        break
                        
                    for tx in items:
                        if tx.get("status") != "ok":
                            continue
                            
                        gas_used = int(tx.get("gas_used", 0))
                        tx_input = tx.get("input", "")
                        to_address = tx.get("to", {}).get("hash") if isinstance(tx.get("to"), dict) else tx.get("to")
                        
                        ts_str = tx.get("timestamp")
                        if ts_str:
                            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                            ts = dt.timestamp()
                            
                            calc = calculate_co2(network_name, gas_used, ts)
                            tx_co2 = calc["co2"]
                            tx_savings = calc["savings_l2"]
                            
                            # Classify transaction
                            activity_type = classify_transaction(tx_input, to_address, network_name)
                            
                            # Update network and global stats
                            network_co2 += tx_co2
                            network_savings += tx_savings
                            tx_count += 1
                            
                            network_activity_types[activity_type]["co2"] += tx_co2
                            network_activity_types[activity_type]["transactions"] += 1
                            
                            global_activity_types[activity_type]["co2"] += tx_co2
                            global_activity_types[activity_type]["transactions"] += 1
                    
                    next_params = data.get("next_page_params")
                    if not next_params:
                        break
                    
                    pages_scanned += 1
                    await asyncio.sleep(0.1)
                except Exception as e:
                    print(f"Error scanning {network_name}: {e}")
                    break
            
            if tx_count > 0:
                breakdown.append({
                    "network": network_name.capitalize(),
                    "co2": round(network_co2, 6),
                    "transactions": tx_count,
                    "savings_l2": round(network_savings, 6),
                    "activity_types": {k: {"co2": round(v["co2"], 6), "transactions": v["transactions"]} 
                                       for k, v in network_activity_types.items() if v["transactions"] > 0}
                })
                total_co2 += network_co2
                total_savings += network_savings

        return {
            "address": address,
            "total_co2": round(total_co2, 6),
            "total_savings": round(total_savings, 6),
            "breakdown": breakdown,
            "activity_types": {k: {"co2": round(v["co2"], 6), "transactions": v["transactions"]} 
                               for k, v in global_activity_types.items() if v["transactions"] > 0},
            "last_updated": datetime.utcnow().isoformat()
        }
