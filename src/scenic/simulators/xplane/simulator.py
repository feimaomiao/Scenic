import logging
import math
import os
import traceback
import warnings
from time import sleep

import scenic.core.errors as errors
from scenic.core.simulators import Simulation, SimulationCreationError, Simulator
from scenic.core.vectors import Vector
from scenic.core.simulators import SimulationCreationError
from scenic.syntax.veneer import verbosePrint

try:
  from xpc import XPlaneConnect
except ImportError as exception:
  raise RuntimeError('The X-Plane interface requires XPlaneConnect.') from exception

class XPlaneSimulator(Simulator):

  def __init__(self):
    super().__init__()

    self.simulation = self.createSimulation(None, maxSteps=0, name='xplane test',
                                            timestep=0)
    self.simulation.setup()
    self.simulation.executeActions([])
    self.simulation.getProperties()
    return

  def createSimulation(self, scene, **kwargs):
    return XPlaneSimulation(scene, **kwargs)

  def destroy(self):
    super().destroy()
    return

class XPlaneSimulation(Simulation):

  def __init__(self, scene, **kwargs):
    # super().__init__(scene, **kwargs)

    self.client = XPlaneConnect()
    try:
      self.client.getDREF("sim/test/test_float")
    except:
      raise RuntimeError("Failed to establish connection to XPlane.")

    return

  def setup(self):
    # super().setup()

    # Set position of the player aircraft
    #       Lat     Lon         Alt   Pitch Roll Yaw Gear
    posi = [37.524, -122.06899, 2500, 0,    0,   0,  1]
    self.client.sendPOSI(posi)
    
    # Set position of a non-player aircraft
    #       Lat       Lon         Alt   Pitch Roll Yaw Gear
    posi = [37.52465, -122.06899, 2500, 0,    20,   0,  1]
    self.client.sendPOSI(posi, 1)

    # Set angle of attack, velocity, and orientation using the DATA command
    data = [\
        [18,   0, -998,   0, -998, -998, -998, -998, -998],\
        [ 3, 130,  130, 130,  130, -998, -998, -998, -998],\
        [16,   0,    0,   0, -998, -998, -998, -998, -998]\
        ]
    self.client.sendDATA(data)

    # Set control surfaces and throttle of the player aircraft using sendCTRL
    print("Setting controls")
    ctrl = [0.0, 0.0, 0.0, 0.8]
    self.client.sendCTRL(ctrl)

    return

  def createObjectInSimulator(self, obj):
    return

  def executeActions(self, allActions):
    client.pauseSim(True)
    sleep(2)

    client.pauseSim(False)

    # Stow landing gear using a dataref
    gear_dref = "sim/cockpit/switches/gear_handle_status"
    client.sendDREF(gear_dref, 0)
    return

  def step(self):
    sleep(4)
    return

  def getProperties(self, obj, properties):
    # Make sure gear was stowed successfully
    gear_status = client.getDREF(gear_dref)
    if gear_status[0] == 0:
        print("Gear stowed")
    else:
        print("Error stowing gear")
    return

  def destroy(self):
    return

if __name__ == "__main__":
  XPlaneSimulator()