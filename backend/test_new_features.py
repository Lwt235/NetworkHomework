#!/usr/bin/env python3
"""
Test script for new features added to the network monitoring system
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.monitor import get_network_load, get_network_traffic
from services.capture import get_packet_analysis, get_protocol_stats
import time

def test_network_load():
    """Test the network load monitoring function"""
    print("\n=== Testing Network Load Monitoring ===")
    try:
        load_data = get_network_load()
        print("✓ Network load function executed successfully")
        print(f"  Upload rate: {load_data['bytes_sent_per_sec']:.2f} bytes/sec")
        print(f"  Download rate: {load_data['bytes_recv_per_sec']:.2f} bytes/sec")
        print(f"  Upload utilization: {load_data['upload_utilization_percent']:.2f}%")
        print(f"  Download utilization: {load_data['download_utilization_percent']:.2f}%")
        print(f"  Total utilization: {load_data['total_utilization_percent']:.2f}%")
        return True
    except Exception as e:
        print(f"✗ Network load test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_network_traffic():
    """Test the network traffic monitoring function"""
    print("\n=== Testing Network Traffic Monitoring ===")
    try:
        traffic_data = get_network_traffic()
        print("✓ Network traffic function executed successfully")
        print(f"  Bytes sent: {traffic_data['bytes_sent']}")
        print(f"  Bytes received: {traffic_data['bytes_recv']}")
        print(f"  Packets sent: {traffic_data['packets_sent']}")
        print(f"  Packets received: {traffic_data['packets_recv']}")
        return True
    except Exception as e:
        print(f"✗ Network traffic test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_speedtest_import():
    """Test that speedtest module can be imported"""
    print("\n=== Testing Speedtest Module ===")
    try:
        import speedtest
        print("✓ Speedtest module imported successfully")
        print(f"  Speedtest version: {speedtest.__version__ if hasattr(speedtest, '__version__') else 'unknown'}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import speedtest: {str(e)}")
        return False

def test_packet_analysis_functions():
    """Test that packet analysis functions can be called (without actual data)"""
    print("\n=== Testing Packet Analysis Functions ===")
    try:
        # These functions require database context, so we just test they're importable
        from services.capture import get_packet_analysis, get_protocol_stats
        print("✓ Packet analysis functions imported successfully")
        return True
    except Exception as e:
        print(f"✗ Packet analysis import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing New Features for Network Monitoring System")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Network Load", test_network_load()))
    results.append(("Network Traffic", test_network_traffic()))
    results.append(("Speedtest Import", test_speedtest_import()))
    results.append(("Packet Analysis", test_packet_analysis_functions()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
