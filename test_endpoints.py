import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("Testing /v1/healthz...")
    try:
        resp = requests.get(f"{BASE_URL}/v1/healthz")
        print(f"Healthz: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    print("\nTesting /v1/metadata...")
    resp = requests.get(f"{BASE_URL}/v1/metadata")
    print(f"Metadata: {resp.status_code} - {resp.json()}")

    print("\nTesting /v1/context...")
    context_payload = {
        "category": {
            "slug": "dentists",
            "offer_catalog": ["Dental Cleaning @ ₹299"],
            "peer_stats": {"avg_ctr": 0.030}
        },
        "merchant": {
            "identity": {"name": "Dr. Meera Clinic"},
            "performance": {"ctr": 0.021}
        },
        "trigger": {
            "id": "trg_001",
            "kind": "perf_dip",
            "payload": {},
            "urgency": 3
        },
        "customer": {
            "identity": {"name": "Priya"}
        }
    }
    resp = requests.post(f"{BASE_URL}/v1/context", json=context_payload)
    print(f"Context Response: {resp.status_code} - {resp.json()}")
    
    if resp.status_code == 200:
        context_id = resp.json().get("context_id")
        
        print("\nTesting /v1/tick...")
        tick_payload = {"context_id": context_id}
        resp = requests.post(f"{BASE_URL}/v1/tick", json=tick_payload)
        print(f"Tick Response: {resp.status_code} - {resp.json()}")

    print("\nTesting /v1/reply...")
    reply_payload = {"merchant_id": "merch_123", "reply_text": "yes"}
    resp = requests.post(f"{BASE_URL}/v1/reply", json=reply_payload)
    print(f"Reply Response: {resp.status_code} - {resp.json()}")

if __name__ == "__main__":
    run_tests()
