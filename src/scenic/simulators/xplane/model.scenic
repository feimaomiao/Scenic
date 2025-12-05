"""Scenic world model for the X-Plane simulator.
"""
from scenic.simulators.xplane.common import *
from scenic.simulators.xplane.simulator import XPlaneSimulator

simulator XPlaneSimulator()

class Plane()
  pass

class BeechcraftBaron58(Plane):
    width : 11.53
    height : 2.97
    length : 9.09
    shape : BoxShape()
    crashed: False