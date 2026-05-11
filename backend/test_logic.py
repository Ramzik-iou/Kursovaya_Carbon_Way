from calculator import calculate_co2, get_analogies
from datetime import datetime

def test_calculator():
    # Test Ethereum Pre-merge
    pre_merge_ts = datetime(2021, 1, 1).timestamp()
    res_pow = calculate_co2("ethereum", 21000, pre_merge_ts)
    print(f"ETH Pre-merge (21k gas): {res_pow['co2']:.6f} kg CO2")
    
    # Test Ethereum Post-merge
    post_merge_ts = datetime(2023, 1, 1).timestamp()
    res_pos = calculate_co2("ethereum", 21000, post_merge_ts)
    print(f"ETH Post-merge (21k gas): {res_pos['co2']:.6f} kg CO2")
    
    # Test Polygon
    res_poly = calculate_co2("polygon", 21000, post_merge_ts)
    print(f"Polygon (21k gas): {res_poly['co2']:.6f} kg CO2, Savings: {res_poly['savings_l2']:.6f} kg CO2")
    
    # Test Analogies
    total = 5.0 # 5 kg CO2
    an = get_analogies(total)
    print(f"Analogies for 5kg CO2: {an}")

if __name__ == "__main__":
    test_calculator()
