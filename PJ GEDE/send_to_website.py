"""
Simple helper to send JSON payloads to the user's website endpoint.
Configure SEALEN_ENDPOINT env var or set endpoint variable below.
"""
import os, requests, json

def send(payload, endpoint=None):
    if endpoint is None:
        endpoint = os.getenv('SEALEN_ENDPOINT', None)
    if not endpoint:
        raise ValueError("No endpoint configured. Set SEALEN_ENDPOINT env var or pass endpoint.")
    r = requests.post(endpoint, json=payload, timeout=5)
    return r.status_code, r.text

if __name__ == "__main__":
    print("Example usage: set SEALEN_ENDPOINT then call send(payload).")
