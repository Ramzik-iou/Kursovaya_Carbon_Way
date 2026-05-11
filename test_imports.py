import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

try:
    from backend.database import init_db, NetworkMetrics, WalletCache
    print("[OK] database.py imported successfully")
except Exception as e:
    print(f"[FAIL] Error importing database.py: {e}")

try:
    from backend.calculator import calculate_co2, calculate_offset_cost, get_analogies
    print("[OK] calculator.py imported successfully")
except Exception as e:
    print(f"[FAIL] Error importing calculator.py: {e}")

try:
    from backend.scanner import BlockscoutScanner, classify_transaction
    print("[OK] scanner.py imported successfully")
except Exception as e:
    print(f"[FAIL] Error importing scanner.py: {e}")

try:
    from backend.intensity_updater import sync_network_intensity, get_random_fluctuation
    print("[OK] intensity_updater.py imported successfully")
except Exception as e:
    print(f"[FAIL] Error importing intensity_updater.py: {e}")

try:
    from backend.schemas import WalletResult, NetworkBreakdown, SyncStatus
    print("[OK] schemas.py imported successfully")
except Exception as e:
    print(f"[FAIL] Error importing schemas.py: {e}")

print("\nAll import tests complete!")
