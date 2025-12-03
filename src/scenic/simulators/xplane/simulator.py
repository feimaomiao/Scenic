import argparse
import logging
import math
import os
import traceback
import warnings

import yaml
from dotmap import DotMap

import scenic.core.errors as errors
from scenic.core.simulators import Simulation, SimulationCreationError, Simulator
from scenic.core.vectors import Vector
from scenic.core.simulators import SimulationCreationError
from scenic.syntax.veneer import verbosePrint

from scenic import scenarioFromFile

from scenic.simulators.xplane.common import *

from xpc import XPlaneConnect

class XPlaneSimulator(Simulator):

  def __init__(self):
    super().__init__()
    return

  def createSimulation(self, scene, **kwargs):
    return XPlaneSimulation(scene, **kwargs)

  def destroy(self):
    super().destroy()
    return

class XPlaneSimulation(Simulation):

  def __init__(self, scene, **kwargs):
    self.agents = []
    self.wrapper = XPlaneWrapper()
    self.client = self.wrapper.client

    super().__init__(scene, **kwargs)

    self.scene = scene
    print(self.scene)
    return

  def setup(self):
    position = self.scene.egoObject.position
    ratioo = self.scene.params["ratioo"]

    # Rotation Matrix.
    R = np.array([
      [0.9201568,  0.3915501],
      [-0.3915501, 0.9201568]
    ])

    # Adjust according to center of runway.
    location_random_2D = R @ np.array([position[0]*ratioo, position[1]*ratioo]) + \
                             np.array([291.85, -32627.15])

    height = ((position[1]*ratioo - (-self.scene.params["real_lengthh"]/2)) / \
             self.scene.params["real_lengthh"]) * (POINTS[0][1]-POINTS[3][1]) + POINTS[3][1] 

    location_random_3D = (location_random_2D[0], height, location_random_2D[1])

    self.wrapper.setLocation(location_random_3D)

    super().setup()
    return

  def createObjectInSimulator(self, obj):
    return

  def executeActions(self, allActions):
    return

  def step(self):
    time.sleep(SLEEP_TIME_SECONDS)
    print("Simulation done!")
    return

  def getProperties(self, obj, properties):
    props = {}

    props["yaw"] = 0
    props["velocity"] = Vector(0, 0, 0)
    props["position"] = Vector(0, 0, 0)
    props["speed"] = 0
    props["roll"] = 0
    props["angularSpeed"] = 0
    props["pitch"] = 0
    props["angularVelocity"] = Vector(0, 0, 0)

    return props

  def destroy(self):
    return