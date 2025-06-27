# reqlytics/fastapi_middleware.py

import time
import requests
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

REQLYTICS_URL = "https://reqlytics-api.onrender.com/api/v1/track"

class api_analytics(BaseHTTPMiddleware):
    def __init__(self, app, api_key, endpoint=REQLYTICS_URL, timeout=2.0, debug=False):
        super().__init__(app)
        self.api_key = api_key
        self.endpoint = endpoint
        self.timeout = timeout
        self.debug = debug

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = int((time.time() - start_time) * 1000)

        payload = {
            "endpoint": str(request.url.path),
            "method": request.method,
            "status_code": response.status_code,
            "response_time": duration
        }

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            requests.post(self.endpoint, json=payload, headers=headers, timeout=self.timeout)
            if self.debug:
                print("[Reqlytics] Logged:", payload)
        except Exception as e:
            if self.debug:
                print("[Reqlytics] Error:", str(e))

        return response