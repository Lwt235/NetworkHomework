#!/usr/bin/env python3
"""Test packet capture permission handling"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.capture import check_capture_permissions, get_permission_instructions

def test_permission_check():
    """Test permission checking functionality"""
    print("Testing Packet Capture Permission Handling")
    print("=" * 50)
    
    # Test 1: Check permissions
    print("\n1. Testing permission check function...")
    try:
        result = check_capture_permissions()
        assert 'has_permission' in result, "Missing 'has_permission' field"
        assert 'message' in result, "Missing 'message' field"
        
        if result['has_permission']:
            print("✓ Packet capture permissions are available")
        else:
            print(f"✓ Permission check correctly detected missing permissions: {result['message']}")
            assert 'instructions' in result, "Missing 'instructions' field when permissions not available"
            print(f"  Instructions provided for {result['instructions']['os']}")
            
    except Exception as e:
        print(f"✗ Permission check failed: {e}")
        return False
    
    # Test 2: Get permission instructions
    print("\n2. Testing permission instructions function...")
    try:
        instructions = get_permission_instructions()
        assert 'os' in instructions, "Missing 'os' field"
        assert 'methods' in instructions, "Missing 'methods' field"
        assert isinstance(instructions['methods'], list), "'methods' should be a list"
        assert len(instructions['methods']) > 0, "'methods' should not be empty"
        
        for method in instructions['methods']:
            assert 'method' in method, "Each method should have 'method' field"
            assert 'command' in method, "Each method should have 'command' field"
            assert 'description' in method, "Each method should have 'description' field"
        
        print(f"✓ Permission instructions available for {instructions['os']}")
        print(f"  Available methods: {len(instructions['methods'])}")
        for i, method in enumerate(instructions['methods'], 1):
            print(f"    {i}. {method['method']}")
            
    except Exception as e:
        print(f"✗ Permission instructions failed: {e}")
        return False
    
    # Test 3: Verify no mock data functions exist
    print("\n3. Verifying mock data generation was removed...")
    try:
        from services import capture
        assert not hasattr(capture, 'generate_mock_packets'), "generate_mock_packets function should be removed"
        print("✓ Mock data generation function successfully removed")
    except AssertionError as e:
        print(f"✗ Mock data function still exists: {e}")
        return False
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("All permission handling tests passed! ✓")
    return True

if __name__ == '__main__':
    try:
        success = test_permission_check()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
