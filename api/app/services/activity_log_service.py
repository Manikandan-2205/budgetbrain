import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.activity_log import ActivityLog
import logging

logger = logging.getLogger(__name__)

class ActivityLogService:
    def __init__(self):
        self.log_file = "activity_logs.json"
        self.max_buffer_size = 50

    def log_activity(
        self,
        user_id: Optional[int],
        action: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[int] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None,
        db: Optional[Session] = None
    ) -> bool:
        """Log an activity - first to JSON file, then to database when buffer is full"""

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
            # First, try to save to database directly if db session is provided
            if db:
                return self._save_to_database(log_entry, db)

            # Otherwise, buffer in JSON file
            buffered_logs = self._load_buffered_logs()
            buffered_logs.append(log_entry)

            # If buffer is full, save to database and clear buffer
            if len(buffered_logs) >= self.max_buffer_size:
                success = self._flush_logs_to_database(buffered_logs)
                if success:
                    self._clear_buffer()
                    logger.info(f"Successfully flushed {len(buffered_logs)} logs to database")
                    return True
                else:
                    logger.error("Failed to flush logs to database, keeping in buffer")
                    return False
            else:
                # Save to buffer file
                self._save_buffered_logs(buffered_logs)
                return True

        except Exception as e:
            logger.error(f"Error logging activity: {str(e)}")
            return False

    def _load_buffered_logs(self) -> List[Dict[str, Any]]:
        """Load buffered logs from JSON file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading buffered logs: {str(e)}")
            return []

    def _save_buffered_logs(self, logs: List[Dict[str, Any]]) -> bool:
        """Save logs to buffer file"""
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
        db = next(get_db())
        try:
            success_count = 0
            for log_entry in logs:
                if self._save_to_database(log_entry, db):
                    success_count += 1
                else:
                    logger.error(f"Failed to save log entry: {log_entry}")

            db.commit()
            logger.info(f"Successfully saved {success_count}/{len(logs)} logs to database")
            return success_count == len(logs)

        except Exception as e:
            db.rollback()
            logger.error(f"Error flushing logs to database: {str(e)}")
            return False
        finally:
            db.close()

    def _save_to_database(self, log_entry: Dict[str, Any], db: Session) -> bool:
        """Save a single log entry to database"""
        try:
            activity_log = ActivityLog(
                user_id=log_entry.get("user_id"),
                action=log_entry["action"],
                resource_type=log_entry.get("resource_type"),
                resource_id=log_entry.get("resource_id"),
                description=log_entry.get("description"),
                log_data=log_entry.get("log_data"),
                ip_address=log_entry.get("ip_address"),
                user_agent=log_entry.get("user_agent"),
                status=log_entry.get("status", "success"),
                error_message=log_entry.get("error_message")
            )

            db.add(activity_log)
            return True

        except Exception as e:
            logger.error(f"Error saving to database: {str(e)}")
            return False

    def get_activity_logs(
        self,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        db: Optional[Session] = None
    ) -> List[Dict[str, Any]]:
        """Get activity logs from database"""
        if not db:
            db = next(get_db())

        try:
            query = db.query(ActivityLog)

            if user_id:
                query = query.filter(ActivityLog.user_id == user_id)
            if action:
                query = query.filter(ActivityLog.action == action)
            if status:
                query = query.filter(ActivityLog.status == status)

            query = query.order_by(ActivityLog.created_at.desc()).limit(limit).offset(offset)

            logs = query.all()

            return [{
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "description": log.description,
                "log_data": log.log_data,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "status": log.status,
                "error_message": log.error_message,
                "created_at": log.created_at.isoformat() if log.created_at else None
            } for log in logs]

        except Exception as e:
            logger.error(f"Error getting activity logs: {str(e)}")
            return []
        finally:
            if not db:
                db.close()

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
            "buffer_file_exists": os.path.exists(self.log_file)
        }

# Global instance
activity_log_service = ActivityLogService()

def get_activity_log_service() -> ActivityLogService:
    """Get the global activity log service instance"""
    return activity_log_service