import math
import time

from scenic.core.simulators import Simulation, Simulator
from scenic.core.vectors import Vector

import numpy as np

from scenic.simulators.xplane.common import *
from scenic.syntax.veneer import verbosePrint


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
    self.wrapper.client.pauseSim(True)
    self.client = self.wrapper.client
    self.scene = scene
    self.maxSteps = kwargs["maxSteps"]
    self.timestep = kwargs["timestep"]
    self.points = scene.params.get("points")
    self.recovered = False
    self.recoverCounter = 100
    # wait while simulator resets
    while self.wrapper.getCrashed():
      time.sleep(1)

    super().__init__(scene, **kwargs)
    self.wrapper.client.pauseSim(False)
    return
  
  def scenicLocation(self):
    """ Generate a random location on the runway based on Scenic scene.
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

    self.wrapper.setLocation((location_random_2D[0],
                              position[2],
                              location_random_2D[1]))
    
    height = ((position[1]- (-self.scene.params["runway_length"]/2)) / \
             self.scene.params["runway_length"]) * (self.points[0][1]-self.points[3][1]) + self.points[3][1]

    location_random_3D = (location_random_2D[0], height, location_random_2D[1])

    self.wrapper.setLocation(location_random_3D)

    # self.wrapper.setWeather(1.0)
    self.wrapper.setWeatherChange(0)
    # self.wrapper.setCloudType(3)

    return

  def setup(self):
    self.wrapper.client.pauseSim(True)
    self.scenicLocation()
    super().setup()
    self.wrapper.client.pauseSim(False)
    return

  """ Assumption is that all objects are agents, and the agents are airplanes.
  """
  def createObjectInSimulator(self, obj):
    obj.blueprint = "Plane"
    obj.crashed = False
    obj.recovered = False
    return

  def executeActions(self, allActions):
    super().executeActions(allActions)
    return

  def step(self):
    time.sleep(self.timestep)
    if self.recovered:
      self.recoverCounter -= 1
      if self.recoverCounter <= 0:
        verbosePrint("Recovering from crash successful", level=3)
        self.wrapper.client.pauseSim(True)
    return
  
  def _isPlane(self, obj):
    return obj.blueprint == "Plane"

  def getProperties(self, obj, properties):
    props = {}

    props["yaw"] = self.client.getDREF("sim/flightmodel/position/beta")[0]
    vx, vz,vy = self.client.getDREFs(["sim/flightmodel/position/local_vx",
                                       "sim/flightmodel/position/local_vy",
                                       "sim/flightmodel/position/local_vz"])
    props["velocity"] = Vector(vx, vy, vz)


    x, z, y = self.client.getDREFs(["sim/flightmodel/position/local_x",
                                     "sim/flightmodel/position/local_y",
                                     "sim/flightmodel/position/local_z"])
    
    # calculate relative position to origin (0,0,0)
    # (0,0,0) is the middle point of self.points
    origin_x = sum([point[0] for point in self.points]) / 4
    origin_z = sum([point[1] for point in self.points]) / 4
    origin_y = sum([point[2] for point in self.points]) / 4
    props["position"] = Vector(x[0] - origin_x, y[0] - origin_y, z[0] - origin_z)
    props["speed"] = self.client.getDREF("sim/flightmodel/position/equivalent_airspeed")[0]
    props["roll"] = self.client.getDREF("sim/flightmodel/position/phi")[0]
    props["pitch"] = self.client.getDREF("sim/flightmodel/position/alpha")[0]
    P, Q, R = self.client.getDREFs(["sim/flightmodel/position/P",
                                  "sim/flightmodel/position/Q",
                                  "sim/flightmodel/position/R"])

    props["angularVelocity"] = Vector(P[0], Q[0], R[0])
    props["angularSpeed"] = math.sqrt(P[0]**2 + Q[0]**2 + R[0]**2)
    
    if self._isPlane(obj):
      obj.crashed = self.wrapper.getCrashed()
      obj.recoverCounter = self.recoverCounter
      obj.recovered = self.recovered

    return props

  def destroy(self):
    return