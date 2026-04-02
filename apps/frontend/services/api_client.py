import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"


def fetch_eco_route(start: str, end: str):
    """
    Calls the backend eco-route endpoint with start/end node IDs.
    Returns the full response with eco path, shortest path, and metrics.
    """
    try:
        payload = {"start": start.strip().upper(), "end": end.strip().upper()}
        response = requests.post(
            f"{BACKEND_URL}/api/v1/eco-route",
            json=payload,
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        else:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            st.error(f"Backend error ({response.status_code}): {detail}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to backend. Make sure FastAPI is running.")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None


def trigger_training():
    """Triggers the model training via the backend endpoint."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/train/trigger",
            timeout=120,
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"Server returned {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "Cannot connect to backend. Is FastAPI running?"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def check_backend_health():
    """Quick health check against the backend health endpoint."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        return response.status_code == 200
    except Exception:
        return False


# ─────────────────────────────────────
# GRAPH MANAGEMENT
# ─────────────────────────────────────

def fetch_graph():
    """Fetch the full city/road graph from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/graph/graph", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None


def smart_add_city(city_name: str):
    """Smart add — just provide a city name. Backend handles everything."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/graph/smart-add",
            json={"city_name": city_name},
            timeout=15,  # geocoding can take a moment
        )
        if response.status_code == 200:
            return response.json()
        else:
            try:
                return response.json()
            except Exception:
                return {"status": "error", "detail": response.text}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "detail": "Cannot connect to backend."}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def add_city(node_id: str, name: str, lat: float, lng: float):
    """Add a new city to the graph."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/graph/cities",
            json={"node_id": node_id, "name": name, "lat": lat, "lng": lng},
            timeout=5,
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def remove_city(node_id: str):
    """Remove a city from the graph."""
    try:
        response = requests.delete(
            f"{BACKEND_URL}/api/v1/graph/cities/{node_id}",
            timeout=5,
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def add_road(from_id: str, to_id: str, distance: float, pollution: float):
    """Add a road between two cities."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/graph/roads",
            json={"from": from_id, "to": to_id, "distance": distance, "pollution": pollution},
            timeout=5,
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def remove_road(from_id: str, to_id: str):
    """Remove a road between two cities."""
    try:
        response = requests.delete(
            f"{BACKEND_URL}/api/v1/graph/roads",
            json={"from": from_id, "to": to_id},
            timeout=5,
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def reset_graph():
    """Reset the graph to defaults."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/graph/graph/reset",
            timeout=5,
        )
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

