# reqlytics/flask_middleware.py

import time
import requests
from flask import request

REQLYTICS_URL = "https://reqlytics-api.onrender.com/api/v1/track"

def api_analytics(api_key, endpoint=REQLYTICS_URL, timeout=2.0, debug=False):
    def middleware(response):
        try:
            start = getattr(request, "_reqlytics_start", None)
            if start is None:
                return response

            duration = int((time.time() - start) * 1000)
            payload = {
                "endpoint": request.path,
                "method": request.method,
                "status_code": response.status_code,
                "response_time": duration
            }

            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json"
            }

            requests.post(endpoint, json=payload, headers=headers, timeout=timeout)

            if debug:
                print("[Reqlytics] Logged:", payload)

        except Exception as e:
            if debug:
                print("[Reqlytics] Error:", str(e))

        return response

    return middleware

def start_timer():
    request._reqlytics_start = time.time()