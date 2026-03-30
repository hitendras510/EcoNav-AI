import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from envs.pollution_env.env import PollutionEnv
from envs.pollution_env.models import RouteAction


env = PollutionEnv()

state = env.reset()
print("Initial State:", state)

action = RouteAction(
    start="Delhi",
    end="Noida",
    mode="bike"
)

obs, reward, done, _ = env.step(action)

print("\nObservation:", obs)
print("Reward:", reward)