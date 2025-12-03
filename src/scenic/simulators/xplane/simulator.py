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

    # self.scenario = scenarioFromFile(scenic_file)
    # self.simulate(self.scenario)

    # self.simulation = self.createSimulation(None, maxSteps=0, name='xplane test', timestep=0)
    # self.simulation.setup()
    # self.simulation.executeActions([])
    # self.simulation.getProperties(None, None)
    return

  def createSimulation(self, scene, **kwargs):
    return XPlaneSimulation(scene, **kwargs)

  def destroy(self):
    super().destroy()
    return

class XPlaneSimulation(Simulation):

  def __init__(self, scene, **kwargs):
    # super().__init__(scene, **kwargs)

    self.wrapper = XPlaneWrapper()
    self.scene = scene
    self.setup()
    return

  def setup(self):
    # super().setup()

    # print(f'ego has foo = {scene.egoObject.width}, {scene.egoObject.position}, {scene.params}')
    position = self.scene.egoObject.position
    ratioo = self.scene.params["ratioo"]
    R = np.array([     # rotation matrix
      [0.9201568,  0.3915501],
      [-0.3915501, 0.9201568]
    ])
    location_random_2D = R @ np.array([position[0]*ratioo, position[1]*ratioo]) + np.array([291.85, -32627.15])  # adjust according to center of runway
    height = ((position[1]*ratioo - (-self.scene.params["real_lengthh"]/2)) / self.scene.params["real_lengthh"]) * (POINTS[0][1]-POINTS[3][1]) + POINTS[3][1] 
    location_random_3D = (location_random_2D[0], height, location_random_2D[1])
    # print(location_random_3D)

    self.wrapper.setLocation(location_random_3D)
    time.sleep(SLEEP_TIME_SECONDS)
    return

  def createObjectInSimulator(self, obj):
    return

  def executeActions(self, allActions):
    self.client.pauseSim(True)
    sleep(2)

    self.client.pauseSim(False)

    # Stow landing gear using a dataref
    self.client.sendDREF("sim/cockpit/switches/gear_handle_status", 0)
    return

  def step(self):
    time.sleep(4)
    return

  def getProperties(self, obj, properties):
    # Make sure gear was stowed successfully
    gear_status = self.client.getDREF("sim/cockpit/switches/gear_handle_status")
    if gear_status[0] == 0:
        print("Gear stowed")
    else:
        print("Error stowing gear")
    return

  def destroy(self):
    return

def load_yaml(filename):
    with open(filename, 'r') as stream:
        options = yaml.safe_load(stream)
    return options