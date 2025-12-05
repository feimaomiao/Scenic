# Load X-Plane world model
from scenic.simulators.xplane.world import *

from scenic.simulators.xplane.model import *

from scenic.simulators.xplane.behaviors import *

from pathlib import Path

import json

import shutil

with open('config.json', 'r') as f:
    config = json.load(f)

fms_path = Path(config["xplane-install"]) / "Output" / "FMS plans"

flight_plan = config["flight-path"]

# copy flight plan to X-Plane FMS plans directory
source = Path(flight_plan)
destination = fms_path / source.name
fms_path.mkdir(parents=True, exist_ok=True)

#remove every other file in the directory 
for item in fms_path.iterdir():
    if item.is_file() and item != destination:
        item.unlink()

shutil.copy2(source, destination)


"""
   In its current state, the model only supports the Beechcraft Baron 58 airplane
   and the LOWS R 15 / R 33 runway, with R15 preferred.
"""
POINTS = config["points"]

class BeechcraftBaron58:
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
