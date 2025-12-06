# Load X-Plane world model
from scenic.simulators.xplane.world import *

from scenic.simulators.xplane.model import *

from scenic.simulators.xplane.behaviors import *

from scenic.simulators.xplane.common import write_flight_plan

from pathlib import Path

import json

import shutil

with open('config.json', 'r') as f:
    config = json.load(f)

flight_plan_string = \
"""I
1100 Version
CYCLE 2406
ADEP LOWS
ADES LOIK
NUMENR 3
1 LOWS ADEP 1411.000000 47.793427 13.003893
11 RADIZ DRCT 14486.000000 47.626286 12.538625
1 LOIK ADES 1586.000000 47.564631 12.127270
"""

# Write flight plan to X-Plane installation directory
xplane_install_path = Path(config["xplane-install"])

write_flight_plan(xplane_install_path, flight_plan_string, config["fpl_name"])


"""
   In its current state, the model only supports the Beechcraft Baron 58 airplane
   and the LOWS R 15 / R 33 runway, with R15 preferred.
"""
POINTS = config["points"]

class BeechcraftBaron58(Plane):
    width :11.53
    height :2.97
    length :9.09
    shape :BoxShape()

param points = POINTS[:4]

startingpoint = (-237.63894653320312, 337.91754150390625, -33869.328125) # Beginning of runway R15

workspace = points_to_workspace(*POINTS)
Runway = workspace

ego = new BeechcraftBaron58 on Runway,
    with behavior FlyRoute(startingpoint)

terminate simulation when (ego.crashed == True)