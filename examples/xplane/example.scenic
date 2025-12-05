# Load X-Plane world model
from scenic.simulators.xplane.world import *

from scenic.simulators.xplane.model import *

POINTS = [
    (850, 350.7986755371094, -31372),                            # top left corner
    (808.9561157226562, 351.1387634277344, -31355.494140625),    # top right corner
    (-225.74005126953125, 337.68798828125, -33897.8203125),      # bottom left corner
    (-266.25006103515625, 337.9598083496094, -33882.296875),     # bottom right corner
]
"""
   In its current state, the model only supports the Beechcraft Baron 58 airplane
   and the LOWS R 15 / R 33 runway, with R15 preferred.
"""

class BeechcraftBaron58:
    width :11.53
    height :2.97
    length :9.09
    shape :BoxShape()

param points = POINTS[:4]
param startingpoint = (291.85, 343.5, -32627.15)                                   # center of runway

workspace = points_to_workspace(*POINTS)
Runway = workspace


ego = new BeechcraftBaron58 on Runway 
