"""Scenic world model for the X-Plane simulator.
"""
from scenic.simulators.xplane.common import *
from scenic.simulators.xplane.simulator import XPlaneSimulator

simulator XPlaneSimulator()

class Plane():
  crashed: False
  recoverCounter: 30
  startingpoint: (0, 0, 0)
  distance: 0
  recovery: 0
  recover_time : 0
  target_coord : (0, 0, 0)