"""
Performance monitoring and optimization utilities
"""

import time
import logging
from typing import Dict, Any, Optional, Callable, TypeVar
from functools import wraps
from contextlib import contextmanager
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None
import threading
from collections import defaultdict, deque
import gc

logger = logging.getLogger(__name__)

T = TypeVar('T')

class PerformanceMonitor:
    """Performance monitoring and metrics collection"""

    def __init__(self, max_metrics: int = 1000):
        self.metrics = defaultdict(lambda: deque(maxlen=max_metrics))
        self.counters = defaultdict(int)
        self.timers = {}
        self.lock = threading.Lock()

    def record_metric(self, name: str, value: float, tags: Optional[Dict[str, Any]] = None):
        """Record a performance metric"""
        with self.lock:
            self.metrics[name].append({
                'value': value,
                'timestamp': time.time(),
                'tags': tags or {}
            })

    def increment_counter(self, name: str, amount: int = 1):
        """Increment a counter"""
        with self.lock:
            self.counters[name] += amount

    def start_timer(self, name: str):
        """Start a timer"""
        with self.lock:
            self.timers[name] = time.time()

    def end_timer(self, name: str) -> float:
        """End a timer and return elapsed time"""
        with self.lock:
            if name in self.timers:
                elapsed = time.time() - self.timers[name]
                del self.timers[name]
                self.record_metric(f"timer.{name}", elapsed)
                return elapsed
            return 0.0

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics"""
        with self.lock:
            summary = {
                'counters': dict(self.counters),
                'timers_active': list(self.timers.keys()),
                'metrics_count': {name: len(values) for name, values in self.metrics.items()}
            }

            # Calculate averages for metrics
            for name, values in self.metrics.items():
                if values:
                    metric_values = [v['value'] for v in values]
                    summary[f'avg_{name}'] = sum(metric_values) / len(metric_values)
                    summary[f'max_{name}'] = max(metric_values)
                    summary[f'min_{name}'] = min(metric_values)

            return summary

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system resource statistics"""
        stats = {'active_threads': threading.active_count()}

        if PSUTIL_AVAILABLE and psutil:
            try:
                stats.update({
                    'cpu_percent': psutil.cpu_percent(interval=0.1),
                    'memory_percent': psutil.virtual_memory().percent,
                    'memory_used_mb': psutil.virtual_memory().used / 1024 / 1024,
                    'memory_available_mb': psutil.virtual_memory().available / 1024 / 1024,
                    'disk_usage_percent': psutil.disk_usage('/').percent,
                })
            except Exception as e:
                logger.error(f"Error getting system stats: {e}")
        else:
            # Fallback stats when psutil is not available
            stats.update({
                'cpu_percent': 0.0,
                'memory_percent': 0.0,
                'memory_used_mb': 0.0,
                'memory_available_mb': 0.0,
                'disk_usage_percent': 0.0,
                'psutil_available': False
            })

        return stats


# Global performance monitor
performance_monitor = PerformanceMonitor()


def performance_monitoring(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator for performance monitoring"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        func_name = f"{func.__module__}.{func.__qualname__}"
        performance_monitor.start_timer(func_name)

        try:
            result = func(*args, **kwargs)
            performance_monitor.end_timer(func_name)
            return result
        except Exception as e:
            performance_monitor.end_timer(func_name)
            performance_monitor.record_metric(f"error.{func_name}", 1.0, {'error_type': type(e).__name__})
            raise

    return wrapper


@contextmanager
def time_operation(operation_name: str):
    """Context manager for timing operations"""
    performance_monitor.start_timer(operation_name)
    try:
        yield
    finally:
        performance_monitor.end_timer(operation_name)


class OptimizedDataStructures:
    """Optimized data structures for performance"""

    @staticmethod
    def create_efficient_cache(max_size: int = 1000):
        """Create an efficient LRU cache"""
        from collections import OrderedDict

        class LRUCache:
            def __init__(self, capacity: int):
                self.cache = OrderedDict()
                self.capacity = capacity

            def get(self, key):
                if key not in self.cache:
                    return None
                self.cache.move_to_end(key)
                return self.cache[key]

            def put(self, key, value):
                if key in self.cache:
                    self.cache.move_to_end(key)
                self.cache[key] = value
                if len(self.cache) > self.capacity:
                    self.cache.popitem(last=False)

            def clear(self):
                self.cache.clear()

            def size(self):
                return len(self.cache)

        return LRUCache(max_size)

    @staticmethod
    def create_batched_processor(batch_size: int = 100):
        """Create a batch processor for efficient bulk operations"""

        class BatchProcessor:
            def __init__(self, batch_size: int, processor_func: Callable):
                self.batch_size = batch_size
                self.processor_func = processor_func
                self.batch = []

            def add(self, item):
                self.batch.append(item)
                if len(self.batch) >= self.batch_size:
                    self._process_batch()

            def flush(self):
                if self.batch:
                    self._process_batch()

            def _process_batch(self):
                try:
                    self.processor_func(self.batch)
                    performance_monitor.record_metric("batch_processed", len(self.batch))
                except Exception as e:
                    logger.error(f"Batch processing error: {e}")
                    performance_monitor.record_metric("batch_error", len(self.batch))
                finally:
                    self.batch.clear()

        return BatchProcessor

    @staticmethod
    def create_memory_efficient_list(max_memory_mb: float = 100):
        """Create memory-efficient list with automatic cleanup"""

        class MemoryEfficientList:
            def __init__(self, max_memory_mb: float):
                self.items = []
                self.max_memory_mb = max_memory_mb
                self.memory_threshold = max_memory_mb * 0.8  # 80% threshold

            def append(self, item):
                self.items.append(item)
                self._check_memory()

            def extend(self, items):
                self.items.extend(items)
                self._check_memory()

            def _check_memory(self):
                # Simple memory check (can be enhanced with actual memory profiling)
                if len(self.items) > 1000:  # Arbitrary threshold
                    # Force garbage collection
                    gc.collect()
                    performance_monitor.record_metric("memory_cleanup", len(self.items))

            def clear(self):
                self.items.clear()
                gc.collect()

            def __len__(self):
                return len(self.items)

            def __getitem__(self, index):
                return self.items[index]

            def __iter__(self):
                return iter(self.items)

        return MemoryEfficientList(max_memory_mb)


class DatabaseOptimizer:
    """Database optimization utilities"""

    @staticmethod
    def create_connection_pool(min_size: int = 5, max_size: int = 20):
        """Create optimized database connection pool settings"""
        return {
            'pool_pre_ping': True,
            'pool_recycle': 300,  # Recycle connections every 5 minutes
            'pool_size': min_size,
            'max_overflow': max_size - min_size,
            'pool_timeout': 30,
            'echo': False  # Disable SQL logging in production
        }

    @staticmethod
    def optimize_query(query, use_selectinload: bool = True):
        """Optimize database queries with eager loading"""
        # This would be implemented based on specific query patterns
        # For now, return the query as-is
        return query

    @staticmethod
    def create_bulk_insert_optimizer(table_class, batch_size: int = 1000):
        """Create bulk insert optimizer"""

        class BulkInsertOptimizer:
            def __init__(self, table_class, batch_size: int):
                self.table_class = table_class
                self.batch_size = batch_size
                self.batch = []

            def add(self, data: Dict[str, Any]):
                self.batch.append(data)
                if len(self.batch) >= self.batch_size:
                    self._execute_bulk_insert()

            def flush(self):
                if self.batch:
                    self._execute_bulk_insert()

            def _execute_bulk_insert(self):
                try:
                    # Bulk insert logic would go here
                    performance_monitor.record_metric("bulk_insert", len(self.batch))
                    self.batch.clear()
                except Exception as e:
                    logger.error(f"Bulk insert error: {e}")
                    performance_monitor.record_metric("bulk_insert_error", len(self.batch))

        return BulkInsertOptimizer(table_class, batch_size)


# Global instances
lru_cache = OptimizedDataStructures.create_efficient_cache()
performance_monitor = PerformanceMonitor()

def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor"""
    return performance_monitor

def get_lru_cache():
    """Get global LRU cache"""
    return lru_cache