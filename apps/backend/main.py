from fastapi import FastAPI
from apps.backend.services.ai_model import choose_best_route

app = FastAPI()


@app.get("/")
def home():
    return {"message": "EcoNav AI Running 🚀"}


@app.get("/route")
def get_best_route():
    # sample routes (later can come from maps API)
    routes = [
        {"path": ["A", "B", "C"], "distance": 5, "traffic": 3},
        {"path": ["A", "D", "C"], "distance": 6, "traffic": 2},
        {"path": ["A", "E", "C"], "distance": 4, "traffic": 6},
    ]

    best, all_routes = choose_best_route(routes)

    return {"best_route": best, "all_routes": all_routes}
