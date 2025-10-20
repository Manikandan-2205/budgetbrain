import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Any
from app.services.activity_log_service import get_activity_log_service

logger = logging.getLogger(__name__)

class LogManager:
    """Manages activity logging with JSON buffer and database persistence"""

    def __init__(self):
        self.activity_logger = get_activity_log_service()
        self.log_file = "activity_logs.json"
        self.max_buffer_size = 50

    def log_activity(
        self,
        user_id: int = None,
        action: str = None,
        resource_type: str = None,
        resource_id: int = None,
        description: str = None,
        metadata: Dict[str, Any] = None,
        ip_address: str = None,
        user_agent: str = None,
        status: str = "success",
        error_message: str = None
    ) -> bool:
        """Log activity with buffer management"""

        # Create log entry
        log_entry = {
            "user_id": user_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "description": description,
            "log_data": metadata,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "status": status,
            "error_message": error_message,
            "created_at": datetime.utcnow().isoformat()
        }

        try:
            # Load existing buffer
            buffered_logs = self._load_buffered_logs()
            buffered_logs.append(log_entry)

            # Check if buffer is full
            if len(buffered_logs) >= self.max_buffer_size:
                # Flush to database
                success = self._flush_logs_to_database(buffered_logs)
                if success:
                    self._clear_buffer()
                    logger.info(f"Successfully flushed {len(buffered_logs)} logs to database")
                    return True
                else:
                    logger.error("Failed to flush logs to database")
                    return False
            else:
                # Save to buffer
                self._save_buffered_logs(buffered_logs)
                return True

        except Exception as e:
            logger.error(f"Error in log_activity: {str(e)}")
            return False

    def _load_buffered_logs(self) -> List[Dict[str, Any]]:
        """Load logs from JSON buffer file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading buffered logs: {str(e)}")
            return []

    def _save_buffered_logs(self, logs: List[Dict[str, Any]]) -> bool:
        """Save logs to JSON buffer file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving buffered logs: {str(e)}")
            return False

    def _clear_buffer(self):
        """Clear the buffer file"""
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
        except Exception as e:
            logger.error(f"Error clearing buffer: {str(e)}")

    def _flush_logs_to_database(self, logs: List[Dict[str, Any]]) -> bool:
        """Flush buffered logs to database"""
        try:
            # Use the activity log service to save to database
            success_count = 0
            for log_entry in logs:
                if self.activity_logger.log_activity(
                    user_id=log_entry.get("user_id"),
                    action=log_entry.get("action"),
                    resource_type=log_entry.get("resource_type"),
                    resource_id=log_entry.get("resource_id"),
                    description=log_entry.get("description"),
                    metadata=log_entry.get("log_data"),
                    ip_address=log_entry.get("ip_address"),
                    user_agent=log_entry.get("user_agent"),
                    status=log_entry.get("status", "success"),
                    error_message=log_entry.get("error_message")
                ):
                    success_count += 1

            logger.info(f"Successfully saved {success_count}/{len(logs)} logs to database")
            return success_count == len(logs)

        except Exception as e:
            logger.error(f"Error flushing logs to database: {str(e)}")
            return False

    def force_flush_buffer(self) -> bool:
        """Force flush all buffered logs to database"""
        buffered_logs = self._load_buffered_logs()
        if not buffered_logs:
            return True

        success = self._flush_logs_to_database(buffered_logs)
        if success:
            self._clear_buffer()
            logger.info(f"Successfully force-flushed {len(buffered_logs)} logs to database")

        return success

    def get_buffer_status(self) -> Dict[str, Any]:
        """Get buffer status"""
        buffered_logs = self._load_buffered_logs()
        return {
            "buffered_count": len(buffered_logs),
            "max_buffer_size": self.max_buffer_size,
            "buffer_file_exists": os.path.exists(self.log_file),
            "buffer_usage_percent": (len(buffered_logs) / self.max_buffer_size) * 100
        }

# Global instance
log_manager = LogManager()

def get_log_manager() -> LogManager:
    """Get the global log manager instance"""
    return log_manager

# Convenience functions for easy logging
def log_user_action(user_id: int, action: str, description: str = None, **kwargs):
    """Log user action"""
    return log_manager.log_activity(
        user_id=user_id,
        action=action,
        description=description,
        **kwargs
    )

def log_system_action(action: str, description: str = None, **kwargs):
    """Log system action"""
    return log_manager.log_activity(
        user_id=None,
        action=action,
        description=description,
        **kwargs
    )