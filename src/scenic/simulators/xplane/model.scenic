"""Scenic world model for the X-Plane simulator.
"""
from scenic.simulators.xplane.common import *
from scenic.simulators.xplane.simulator import XPlaneSimulator

simulator XPlaneSimulator()

class Plane():
  crashed: False