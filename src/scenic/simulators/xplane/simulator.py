import argparse
import logging
import math
import os
import traceback
import warnings
import time

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
    return

  def setup(self):
    # super().setup()

    # Set position of the player aircraft
    #       Lat     Lon         Alt   Pitch Roll Yaw Gear
    posi = [47.80460447599387, 12.996827345547088,
            429.2803463173907, 0.6177443265914917, 
            -0.6730020046234131, 156.9822235107422, 1.0]
    self.client.sendPOSI(posi)

    # Set angle of attack, velocity, and orientation using the DATA command
    data = [\
        [18,   0, -998,   0, -998, -998, -998, -998, -998],\
        [ 3, 130,  130, 130,  130, -998, -998, -998, -998],\
        [16,   0,    0,   0, -998, -998, -998, -998, -998]\
        ]
    self.client.sendDATA(data)

    # Set control surfaces and throttle of the player aircraft using sendCTRL
    ctrl = [0.0, 0.0, 0.0, 0.8]
    self.client.sendCTRL(ctrl)

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