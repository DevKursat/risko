"""
Simple metrics collection middleware for API monitoring.
In production, use Prometheus or similar monitoring solutions.
"""
import time
import json
from collections import defaultdict, deque
from typing import Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.request_count = defaultdict(int)
        self.response_times = defaultdict(deque)
        self.error_count = defaultdict(int)
        self.start_time = time.time()
        
        # Keep only last 1000 response times per endpoint
        self.max_response_times = 1000
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url.path
        method = request.method
        endpoint = f"{method} {path}"
        
        # Count request
        self.request_count[endpoint] += 1
        
        response = await call_next(request)
        
        # Calculate response time
        response_time = time.time() - start_time
        
        # Store response time (keep only last N measurements)
        if len(self.response_times[endpoint]) >= self.max_response_times:
            self.response_times[endpoint].popleft()
        self.response_times[endpoint].append(response_time)
        
        # Count errors
        if response.status_code >= 400:
            self.error_count[endpoint] += 1
        
        # Add response time header
        response.headers["X-Response-Time"] = f"{response_time:.3f}s"
        
        return response
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        uptime = time.time() - self.start_time
        
        metrics = {
            "uptime_seconds": round(uptime, 2),
            "total_requests": sum(self.request_count.values()),
            "total_errors": sum(self.error_count.values()),
            "endpoints": {}
        }
        
        for endpoint in self.request_count.keys():
            response_times = list(self.response_times[endpoint])
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            metrics["endpoints"][endpoint] = {
                "request_count": self.request_count[endpoint],
                "error_count": self.error_count[endpoint],
                "avg_response_time": round(avg_response_time, 3),
                "min_response_time": round(min(response_times), 3) if response_times else 0,
                "max_response_time": round(max(response_times), 3) if response_times else 0
            }
        
        return metrics

# Global metrics instance
metrics_middleware = None

def get_metrics_middleware():
    global metrics_middleware
    return metrics_middleware

def set_metrics_middleware(middleware):
    global metrics_middleware
    metrics_middleware = middleware