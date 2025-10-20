#!/usr/bin/env python3
"""
Test script to verify activity logging functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.services.log_manager import get_log_manager
from app.services.activity_log_service import get_activity_log_service

def test_log_manager():
    """Test the log manager functionality"""
    print("Testing Log Manager...")

    log_manager = get_log_manager()

    # Test logging some activities
    for i in range(55):  # More than buffer size to trigger flush
        success = log_manager.log_activity(
            user_id=1 if i % 2 == 0 else None,
            action=f"test_action_{i}",
            description=f"Test activity number {i}",
            resource_type="test",
            resource_id=i,
            status="success" if i % 3 != 0 else "failed",
            metadata={"test_key": f"value_{i}"}
        )
        print(f"Log {i}: {'OK' if success else 'FAIL'}")

    # Check buffer status
    status = log_manager.get_buffer_status()
    print(f"\nBuffer Status: {status}")

    # Force flush remaining logs
    print("\nForcing flush of remaining logs...")
    flush_success = log_manager.force_flush_buffer()
    print(f"Flush result: {'OK' if flush_success else 'FAIL'}")

    # Check final buffer status
    final_status = log_manager.get_buffer_status()
    print(f"Final Buffer Status: {final_status}")

def test_activity_log_service():
    """Test the activity log service directly"""
    print("\n\nTesting Activity Log Service...")

    activity_logger = get_activity_log_service()

    # Test direct database logging
    success = activity_logger.log_activity(
        user_id=1,
        action="direct_test",
        description="Direct database test",
        status="success"
    )
    print(f"Direct DB log: {'OK' if success else 'FAIL'}")

    # Test retrieving logs
    logs = activity_logger.get_activity_logs(limit=5)
    print(f"Retrieved {len(logs)} logs from database")

    for log in logs[-3:]:  # Show last 3 logs
        print(f"  - {log['action']}: {log['description'][:50]}...")

if __name__ == "__main__":
    try:
        test_log_manager()
        test_activity_log_service()
        print("\n[SUCCESS] All tests completed successfully!")
    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()