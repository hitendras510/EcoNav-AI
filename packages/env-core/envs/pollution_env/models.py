from pydantic import BaseModel
from typing import List

# action sent by agent 
class RouteAction(BaseModel):
    start: str
    end: str
    mode: str # car, bus, train
    
# WHAT environment will return
class RouteObservation(BaseModel):
    path: List[str]
    avg_aqi: int
    exposure: float
    score: float
     
#Internal env. state 
class EnvState(BaseModel):
    current_location: str
    total_exposure: float 