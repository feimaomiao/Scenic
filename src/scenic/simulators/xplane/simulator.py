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
    self.scene = scene
    self.maxSteps = kwargs["maxSteps"]
    self.timestep = kwargs["timestep"]
    self.points = scene.params.get("points")

    super().__init__(scene, **kwargs)
    return

  def setup(self):
    """The setup function places the plane on a random location on the runway
    """
    position = self.scene.egoObject.position

    # Calculate rotation matrix from the four rectangle points.
    p0 = self.points[0]  # top left
    p1 = self.points[1]  # top right
    p2 = self.points[2]  # bottom left
    p3 = self.points[3]  # bottom right

    # Calculate the along-runway direction (from bottom to top) in X-Plane coordinates.
    # This determines how Scenic's y-axis (along runway) maps to X-Plane's coordinate system.
    bottom_center_x = (p2[0] + p3[0]) / 2
    bottom_center_z = (p2[2] + p3[2]) / 2
    top_center_x = (p0[0] + p1[0]) / 2
    top_center_z = (p0[2] + p1[2]) / 2

    runway_dx = top_center_x - bottom_center_x
    runway_dz = top_center_z - bottom_center_z

    # Calculate rotation angle of the runway.
    angle = np.arctan2(runway_dz, runway_dx)

    # Build rotation matrix that maps Scenic coordinates to X-Plane coordinates.
    # Scenic's x-axis (cross-runway) maps to perpendicular of runway direction.
    # Scenic's y-axis (along-runway) maps to runway direction.
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    R = np.array([
      [sin_theta,   cos_theta],
      [-cos_theta,  sin_theta]
    ])

    # Calculate center of runway from the four corners.
    center_x = (p0[0] + p1[0] + p2[0] + p3[0]) / 4
    center_z = (p0[2] + p1[2] + p2[2] + p3[2]) / 4

    # Adjust according to center of runway.
    location_random_2D = R @ np.array([position[0], position[1]]) + \
                             np.array([center_x, center_z])

    height = ((position[1]- (-self.scene.params["runway_length"]/2)) / \
             self.scene.params["runway_length"]) * (self.points[0][1]-self.points[3][1]) + self.points[3][1]

    location_random_3D = (location_random_2D[0], height, location_random_2D[1])

    self.wrapper.setLocation(location_random_3D)

    super().setup()
    return

  def createObjectInSimulator(self, obj):
    return

  def executeActions(self, allActions):
    return

  def step(self):
    # self.wrapper.client.pauseSim(True)

    # `self.timestep` has a value of 1 by default.
    time.sleep(self.timestep)

    # self.wrapper.client.pauseSim(False)
    return

  def getProperties(self, obj, properties):
    props = {}

    # print(self.client.getDREF("sim/flightmodel/position/beta"))
    props["yaw"] = self.client.getDREF("sim/flightmodel/position/beta")[0]
    vx, vy, vz = self.client.getDREFs(["sim/flightmodel/position/local_vx",
                                       "sim/flightmodel/position/local_vy",
                                       "sim/flightmodel/position/local_vz"])
    props["velocity"] = Vector(vx, vy, vz)
    x, y, z = self.client.getDREFs(["sim/flightmodel/position/local_x",
                                     "sim/flightmodel/position/local_y",
                                     "sim/flightmodel/position/local_z"])
    props["position"] = Vector(x, y, z)
    props["speed"] = self.client.getDREF("sim/flightmodel/position/equivalent_airspeed")[0]
    props["roll"] = self.client.getDREF("sim/flightmodel/position/phi")[0]
    props["angularSpeed"] = self.client.getDREF("sim/flightmodel/position/equivalent_airspeed")[0]
    props["pitch"] = self.client.getDREF("sim/flightmodel/position/alpha")[0]
    props["angularVelocity"] = Vector(vx,vy,vz)

    return props

  def destroy(self):
    return