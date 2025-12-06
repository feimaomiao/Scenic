# Load X-Plane world model
import itertools
import json
from pathlib import Path
import shutil

from scenic.simulators.xplane.behaviors import *
from scenic.simulators.xplane.common import write_flight_plan
from scenic.simulators.xplane.model import *
from scenic.simulators.xplane.world import *

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

conf_errors = config.get("possible_errors")

recovery = DiscreteRange(10, 30)

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

failureheight = DiscreteRange(150,500)

workspace = points_to_workspace(*POINTS)
Runway = workspace

ego = new BeechcraftBaron58 on Runway,
    with behavior FlyErrorAtHeight(startingpoint, failureheight, errors=conf_errors, recovery=recovery),

record (ego.position) as position
record (ego.velocity) as velocity
record (ego.speed) as speed
record (ego.angularVelocity) as angularVelocity
record (ego.angularSpeed) as angularSpeed
record (ego.roll) as roll
record (ego.pitch) as pitch
record (ego.yaw) as yaw

record (ego.recoverCounter) as "Recovery Counter"

# These valuesdoesn't get recorded until the beginning or middle steps of the simulation.
# Thus, getting the initial value using `record initial` will return the uninitialized values of
# (0, 0, 0), 0, or "", depending on the value type.
#
record final (ego.startingpoint) as "Starting Point"
record final (ego.recovery) as "Recovery Time (seconds)"
record final (ego.height) as "Height to Failure"
record final (ego.errors) as "Errors"
record final (ego.error_count) as "Error Count"

record final (ego.crashed) as "Final Crashed State"
record final (ego.recovered) as "Final Recovered State"

terminate simulation when (ego.crashed == True or ego.recovered == -1)