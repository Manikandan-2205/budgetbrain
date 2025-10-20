"""
Performance monitoring middleware for FastAPI
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from app.core.performance import get_performance_monitor

logger = logging.getLogger(__name__)

class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring API performance"""

    def __init__(self, app: Callable):
        super().__init__(app)
        self.performance_monitor = get_performance_monitor()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Record request start
        start_time = time.time()
        path = request.url.path
        method = request.method

        # Track concurrent requests
        self.performance_monitor.increment_counter("requests_total")
        self.performance_monitor.increment_counter(f"requests_method_{method}")

        try:
            # Process request
            response = await call_next(request)

            # Calculate response time
            response_time = time.time() - start_time

            # Record metrics
            self.performance_monitor.record_metric(
                "request_duration",
                response_time,
                {
                    "method": method,
                    "path": path,
                    "status_code": response.status_code
                }
            )

            # Track response status
            self.performance_monitor.increment_counter(f"responses_{response.status_code}")

            # Log slow requests
            if response_time > 1.0:  # More than 1 second
                logger.warning(".2f")

            # Log very slow requests
            if response_time > 5.0:  # More than 5 seconds
                logger.error(".2f")

            return response

        except Exception as e:
            # Record error metrics
            response_time = time.time() - start_time
            self.performance_monitor.record_metric(
                "request_error_duration",
                response_time,
                {
                    "method": method,
                    "path": path,
                    "error_type": type(e).__name__
                }
            )
            self.performance_monitor.increment_counter("requests_error")

            # Re-raise the exception
            raise


class RequestCachingMiddleware(BaseHTTPMiddleware):
    """Middleware for request caching"""

    def __init__(self, app: Callable, cache_timeout: int = 300):
        super().__init__(app)
        self.cache_timeout = cache_timeout
        self.cache = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)

        # Create cache key
        cache_key = f"{request.method}:{request.url.path}?{request.url.query}"

        # Check cache
        if cache_key in self.cache:
            cached_response, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_timeout:
                # Return cached response
                from app.core.performance import get_performance_monitor
                get_performance_monitor().increment_counter("cache_hit")
                return cached_response

        # Process request
        response = await call_next(request)

        # Cache successful GET responses
        if response.status_code == 200:
            self.cache[cache_key] = (response, time.time())
            from app.core.performance import get_performance_monitor
            get_performance_monitor().increment_counter("cache_miss")

        return response


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""

    def __init__(self, app: Callable, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}
        self.window_size = 60  # 1 minute window

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client identifier (IP address)
        client_ip = request.client.host if request.client else "unknown"

        # Clean old requests
        current_time = time.time()
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < self.window_size
            ]

        # Check rate limit
        if client_ip in self.requests and len(self.requests[client_ip]) >= self.requests_per_minute:
            from app.core.exceptions import RateLimitError
            from app.core.performance import get_performance_monitor
            get_performance_monitor().increment_counter("rate_limit_exceeded")
            raise RateLimitError(f"Rate limit exceeded: {self.requests_per_minute} requests per minute")

        # Record request
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(current_time)

        return await call_next(request)


class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    """Global exception handling middleware"""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            from app.core.exceptions import (
                BudgetBrainException,
                handle_budgetbrain_exception,
                create_error_response
            )
            from app.core.performance import get_performance_monitor
            from fastapi import HTTPException
            import traceback

            # Record error metrics
            performance_monitor = get_performance_monitor()
            performance_monitor.increment_counter("exceptions_total")
            performance_monitor.record_metric(
                "exception_handled",
                1.0,
                {
                    "exception_type": type(e).__name__,
                    "path": request.url.path,
                    "method": request.method
                }
            )

            # Log the error
            logger.error(f"Unhandled exception: {type(e).__name__}: {str(e)}")
            logger.error(f"Request: {request.method} {request.url.path}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            # Handle BudgetBrain exceptions
            if isinstance(e, BudgetBrainException):
                raise handle_budgetbrain_exception(e)

            # Handle HTTP exceptions
            if isinstance(e, HTTPException):
                raise e

            # Handle other exceptions
            raise HTTPException(
                status_code=500,
                detail=create_error_response(
                    "Internal server error",
                    "InternalServerError",
                    500,
                    {"error_type": type(e).__name__}
                )
            )