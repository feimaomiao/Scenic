"""Simulator interface"""

"""
Introduction to Simulator Interface

This file illustrates the basics on how to 
implement the Simultor and Simulation class for your
Scenic interface. The docstrings in each function
and class gives a brief description on what you should
write in each function and gives examples where needed.

"""
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
  from xpc import XPlaneConnect # type: ignore
except ImportError as exception:
  raise RuntimeError('The X-Plane interface requires XPlaneConnect.') from exception

class TemplateSimulator(Simulator):

  def __init__(self):
    super().__init__()
    return

  def createSimulation(self, scene, **kwargs):
    return TemplateSimulation(scene, **kwargs)

  def destroy(self):
    super().destroy()
    return

class TemplateSimulation(Simulation):

  def __init__(self, scene, **kwargs):
    super().__init__(scene, **kwargs)
    return

  def setup(self):
    # Calls createObjectInSimulator for each object
    super().setup()
    return

  def createObjectInSimulator(self, obj):
    return

  def executeActions(self, allActions):
    for agent, actions in allActions.items():
        for action in actions:
            action.applyTo(agent, self)
    return

  def step(self):
    return

  def getProperties(self, obj, properties):
    return

  def destroy(self):
    return

if __name__ == "__main__":
  pass