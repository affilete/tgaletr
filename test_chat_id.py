"""
Test Chat ID parsing and handling.
Tests backward compatibility and proper integer conversion.
"""

import sys
import os
import tempfile
from pathlib import Path
import uuid

# Add parent directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from settings_manager import SettingsManager
from config import DEFAULT_CHAT_ID


def test_chat_id_integer_conversion():
    """Test: Chat ID is properly converted to integer."""
    print("\n" + "="*80)
    print("TEST: Chat ID Integer Conversion")
    print("="*80)
    
    # Create temporary settings file in current directory
    temp_file = f"test_settings_{uuid.uuid4().hex}.json"
    
    try:
        settings = SettingsManager(temp_file)
        
        # Test 1: Set string chat ID (backward compatibility)
        print("\n1. Testing string chat ID (backward compatibility)...")
        settings.chat_id = "-1003892216818"
        result = settings.chat_id
        print(f"   Input: '-1003892216818' (string)")
        print(f"   Output: {result} (type: {type(result).__name__})")
        assert isinstance(result, int), f"Expected int, got {type(result)}"
        assert result == -1003892216818, f"Expected -1003892216818, got {result}"
        print("   ✅ PASSED")
        
        # Test 2: Set integer chat ID
        print("\n2. Testing integer chat ID...")
        settings.chat_id = -1001234567890
        result = settings.chat_id
        print(f"   Input: -1001234567890 (int)")
        print(f"   Output: {result} (type: {type(result).__name__})")
        assert isinstance(result, int), f"Expected int, got {type(result)}"
        assert result == -1001234567890, f"Expected -1001234567890, got {result}"
        print("   ✅ PASSED")
        
        # Test 3: Positive chat ID (private chat)
        print("\n3. Testing positive chat ID (private chat)...")
        settings.chat_id = 123456789
        result = settings.chat_id
        print(f"   Input: 123456789 (int)")
        print(f"   Output: {result} (type: {type(result).__name__})")
        assert isinstance(result, int), f"Expected int, got {type(result)}"
        assert result == 123456789, f"Expected 123456789, got {result}"
        print("   ✅ PASSED")
        
        # Test 4: Invalid chat ID (zero) should raise error
        print("\n4. Testing invalid chat ID (zero)...")
        try:
            settings.chat_id = 0
            print("   ❌ FAILED - Should have raised ValueError")
            return False
        except ValueError as e:
            print(f"   Correctly raised ValueError: {e}")
            print("   ✅ PASSED")
        
        # Test 5: Invalid chat ID (non-numeric string) should raise error
        print("\n5. Testing invalid chat ID (non-numeric string)...")
        try:
            settings.chat_id = "not_a_number"
            print("   ❌ FAILED - Should have raised ValueError")
            return False
        except ValueError as e:
            print(f"   Correctly raised ValueError: {e}")
            print("   ✅ PASSED")
        
        print("\n✅ ALL TESTS PASSED")
        return True
        
    finally:
        # Cleanup
        Path(temp_file).unlink(missing_ok=True)


def test_default_chat_id_from_config():
    """Test: DEFAULT_CHAT_ID from config is an integer."""
    print("\n" + "="*80)
    print("TEST: DEFAULT_CHAT_ID from config.py")
    print("="*80)
    
    print(f"\nDEFAULT_CHAT_ID: {DEFAULT_CHAT_ID}")
    print(f"Type: {type(DEFAULT_CHAT_ID).__name__}")
    
    assert isinstance(DEFAULT_CHAT_ID, int), f"Expected int, got {type(DEFAULT_CHAT_ID)}"
    print("✅ DEFAULT_CHAT_ID is an integer")
    
    return True


def test_backward_compatibility():
    """Test: Settings with old string format are converted properly."""
    print("\n" + "="*80)
    print("TEST: Backward Compatibility")
    print("="*80)
    
    # Create temporary settings file with old format (string)
    temp_file = f"test_settings_old_{uuid.uuid4().hex}.json"
    
    try:
        # Write old-style settings with string chat_id
        with open(temp_file, 'w') as f:
            f.write('{"chat_id": "-1003892216818", "alerts_enabled": false}')
        
        settings = SettingsManager(temp_file)
        result = settings.chat_id
        
        print(f"\nLoaded old-format chat_id from file: '{result}'")
        print(f"Type after loading: {type(result).__name__}")
        
        assert isinstance(result, int), f"Expected int, got {type(result)}"
        assert result == -1003892216818, f"Expected -1003892216818, got {result}"
        print("✅ Old string format correctly converted to integer")
        
        return True
        
    finally:
        # Cleanup
        Path(temp_file).unlink(missing_ok=True)


def run_all_tests():
    """Run all chat ID tests."""
    print("=" * 80)
    print("Chat ID Handling Tests")
    print("=" * 80)
    
    tests = [
        ("DEFAULT_CHAT_ID Type Check", test_default_chat_id_from_config),
        ("Integer Conversion", test_chat_id_integer_conversion),
        ("Backward Compatibility", test_backward_compatibility),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASSED" if result else "FAILED", None))
        except Exception as e:
            print(f"\n❌ TEST FAILED: {test_name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
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
