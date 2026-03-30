from typing import Tuple
import random

from .models import RouteAction, RouteObservation, EnvState

try:
        from env_core.core.env_graph import get_route
except ImportError:
        def get_route(start, end):
            return [start,"mid_point", end]

class PollutionEnv:
    def __init__(self):
        self.state = None

    def reset(self) -> EnvState:
        """
        Initialize environment
        """
        self.state = EnvState( #st a new episode
            current_location="START",
            total_exposure=0.0
        )
        return self.state

    def step(self, action: RouteAction) -> Tuple[RouteObservation, float, bool, dict]:
        """
        Execute one step in environment
        """

        #  Simulate a route
        path = [action.start, action.end]

        #  Simulate AQI values (temporary)
        aqi_values = [random.randint(50, 300) for _ in path]
        avg_aqi = sum(aqi_values) / len(aqi_values)

        #  Exposure calculation
        duration = 30  # minutes (fixed for now)
        exposure = avg_aqi * duration

        #  Score (normalize)
        max_exposure = 10000
        score = max(0, 100 - (exposure / max_exposure) * 100)

        # Update state
        self.state.current_location = action.end
        self.state.total_exposure += exposure

        #  Reward (CRITICAL DESIGN)
        reward = -exposure  # lower exposure = better , (RL agents will try to maximize reward)

        #  Observation
        observation = RouteObservation(
            path=path,
            avg_aqi=avg_aqi,
            exposure=exposure,
            score=score
        )

        done = True  # single-step for now
        
   
        return observation, reward, done, {}