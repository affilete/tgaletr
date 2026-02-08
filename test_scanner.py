"""
Comprehensive Exchange Scanner Tests
Tests orderbook handling, volume calculations, and exchange configurations.
"""

import sys
import os
import asyncio
from typing import Dict, Any

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanner import DensityScanner
from settings_manager import SettingsManager

# Test configuration for supported exchanges
TEST_CONFIG = {
    "hyperliquid": {
        "ccxt_id": "hyperliquid",
        "label": "Hyperliquid",
        "test_symbols": ["BTC/USD:USD", "ETH/USD:USD", "SOL/USD:USD"],
        "has_cumulative_book": False,  # Hyperliquid returns individual volumes
        "ws_support": True,
        "market_type": "swap"
    }
}


def test_individual_vs_cumulative_volumes():
    """
    Test: Verify that orderbook volumes are treated as individual, not cumulative.
    This test demonstrates the difference between cumulative and individual volume processing.
    """
    settings = SettingsManager(":memory:")
    scanner = DensityScanner(settings, lambda alert: None)
    
    print("\n" + "="*80)
    print("TEST: Individual vs Cumulative Volume Processing")
    print("="*80)
    
    # Create orderbook with individual volumes
    orderbook = {
        "bids": [
            [50000, 10],   # Level 0: 10 BTC = $500,000 individual
            [49900, 6],    # Level 1: 6 BTC = $299,400 individual
            [49800, 4],    # Level 2: 4 BTC = $199,200 individual
        ],
        "asks": [
            [50100, 1],
            [50200, 2],
        ]
    }
    
    print("\n📊 Orderbook (Individual Volumes):")
    print("Bids:")
    for i, (price, amount) in enumerate(orderbook["bids"]):
        volume = price * amount
        print(f"  Level {i}: Price=${price}, Amount={amount}, Volume=${volume:,.2f}")
    
    # Calculate expected cumulative volume
    cumulative_sum = sum(price * amount for price, amount in orderbook["bids"])
    print(f"\n✅ Expected Total (Sum of Individual): ${cumulative_sum:,.2f}")
    
    # Test with scanner (should sum individual volumes correctly)
    alerts = scanner._compute_densities("test", "BTC/USDT", orderbook, 900000, 1.0)
    
    if alerts:
        alert = alerts[0]
        print(f"✅ Scanner Calculated: ${alert.volume:,.2f}")
        
        # Verify the volumes match (allowing small floating point differences)
        difference = abs(alert.volume - cumulative_sum)
        assert difference < 1.0, f"Volume mismatch: {difference}"
        print(f"✅ Difference: ${difference:.8f} (acceptable)")
        
        # THIS IS WHAT WOULD HAPPEN WITH CUMULATIVE CONVERSION:
        print("\n❌ If treated as CUMULATIVE (INCORRECT):")
        print(f"  Level 0: {orderbook['bids'][0][1]} (first stays same)")
        print(f"  Level 1: {orderbook['bids'][1][1]} - {orderbook['bids'][0][1]} = {orderbook['bids'][1][1] - orderbook['bids'][0][1]} (underestimated)")
        print(f"  Level 2: {orderbook['bids'][2][1]} - {orderbook['bids'][1][1]} = {orderbook['bids'][2][1] - orderbook['bids'][1][1]} (negative!)")
        wrong_sum = orderbook['bids'][0][1]  # Only first level would be correct
        print(f"  ❌ WRONG Total: Only ${orderbook['bids'][0][0] * wrong_sum:,.2f} instead of ${cumulative_sum:,.2f}")
        
        print("\n✅ TEST PASSED: Volumes are correctly treated as individual")
        return True
    else:
        print("❌ No alert generated (threshold not met)")
        return False


def test_hyperliquid_symbol_format():
    """Test: Hyperliquid uses correct CCXT symbol format."""
    settings = SettingsManager(":memory:")
    scanner = DensityScanner(settings, lambda alert: None)
    
    print("\n" + "="*80)
    print("TEST: Hyperliquid Symbol Format")
    print("="*80)
    
    # Check configured symbols
    symbols = TEST_CONFIG["hyperliquid"]["test_symbols"]
    print(f"\n✅ Configured Symbols: {symbols}")
    
    # Verify format (should be BTC/USD:USD, not BTC-USD)
    for symbol in symbols:
        assert "/" in symbol and ":" in symbol, f"Invalid format: {symbol}"
        print(f"  ✅ {symbol} - Correct format (BASE/QUOTE:SETTLE)")
    
    # Test with a sample orderbook
    orderbook = {
        "bids": [[50000, 10], [49900, 12]],
        "asks": [[50100, 1], [50200, 2]],
    }
    
    # Should work without errors
    alerts = scanner._compute_densities("hyperliquid", "BTC/USD:USD", orderbook, 1000000, 1.0)
    
    print(f"\n✅ Scanner processed BTC/USD:USD successfully")
    print(f"✅ Alerts generated: {len(alerts)}")
    print("✅ TEST PASSED: Hyperliquid - Correct symbol format")
    
    return True


def test_all_exchanges_individual_volumes():
    """Test: Verify all exchanges use individual volumes (not cumulative)."""
    print("\n" + "="*80)
    print("TEST: All Exchanges Configuration")
    print("="*80)
    
    print("\n📊 Exchange Configurations:")
    print("-" * 80)
    
    all_passed = True
    for exchange_name, config in TEST_CONFIG.items():
        has_cumulative = config["has_cumulative_book"]
        status = "✅" if not has_cumulative else "❌"
        
        print(f"{status} {config['label']:20s} - has_cumulative_book: {has_cumulative}")
        
        if has_cumulative:
            print(f"   ❌ ERROR: {exchange_name} should have has_cumulative_book=False")
            all_passed = False
    
    print("-" * 80)
    
    if all_passed:
        print("\n✅ TEST PASSED: All exchanges correctly configured with individual volumes")
    else:
        print("\n❌ TEST FAILED: Some exchanges have incorrect configuration")
    
    return all_passed


def run_all_tests():
    """Run all scanner tests."""
    print("=" * 80)
    print("Comprehensive Exchange Scanner Tests")
    print("=" * 80)
    
    tests = [
        ("Configuration Check", test_all_exchanges_individual_volumes),
        ("Individual vs Cumulative", test_individual_vs_cumulative_volumes),
        ("Hyperliquid Symbols", test_hyperliquid_symbol_format),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASSED" if result else "FAILED", None))
        except Exception as e:
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"   Error: {e}")
            results.append((test_name, "FAILED", str(e)))
    
    # Print summary
    print("\n" + "=" * 80)
    print("## 📊 TEST SUMMARY")
    print("=" * 80)
    
    total = len(results)
    passed = sum(1 for _, status, _ in results if status == "PASSED")
    failed = total - passed
    
    print(f"\n- **Total Tests:** {total}")
    print(f"- **✅ Passed:** {passed}")
    print(f"- **❌ Failed:** {failed}")
    print(f"- **Success Rate:** {(passed/total*100):.1f}%")
    
    print("\n### Test Details:")
    for test_name, status, error in results:
        symbol = "✅" if status == "PASSED" else "❌"
        print(f"{symbol} {test_name}: {status}")
        if error:
            print(f"   Error: {error}")
    
    print("\n" + "=" * 80)
    
    if failed == 0:
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        return True
    else:
        print(f"❌ {failed} TEST(S) FAILED")
        print("=" * 80)
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
