""" This script gets the corners of the runway for the LOWS R 15 airport runway assumping
    that the player is flying the Beechcraft Baron 58 aircraft.
"""
from time import sleep
import numpy as np
import argparse
from xpc import XPlaneConnect
from common import *

from scenic import scenarioFromFile

SLEEP_TIME_SECONDS = 3

class XPlaneWrapper():
  X_DREF = "sim/flightmodel/position/local_x"
  Y_DREF = "sim/flightmodel/position/local_y"
  Z_DREF = "sim/flightmodel/position/local_z"
  COORDS_DREFS = [X_DREF, Y_DREF, Z_DREF]

  def __init__(self):
    self.client = XPlaneConnect()
    return

  def getPosition(self):
    position = self.client.getDREFs(self.COORDS_DREFS)
    return tuple([int(coord[0]) for coord in position])

  def setOffset(self, dref, offset):
    self.client.sendDREF(dref, self.client.getDREF(dref)[0] + offset)
    return

  def setLocation(self, location):
    self.client.sendDREFs(self.COORDS_DREFS, [location[0], location[1], location[2]])
    return


if __name__ == "__main__":
  client = XPlaneWrapper()

  # CENTER = client.getPosition()
  # print(CENTER)

  locations = POINTS

  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--scenic-file', help='scenic file')
  args = parser.parse_args()
  scenic_file=args.scenic_file
  scenario = scenarioFromFile(scenic_file)
  # print(scenario)
  for i in range(10):
    scene, numIterations = scenario.generate()
    # print(f'ego has foo = {scene.egoObject.width}, {scene.egoObject.position}, {scene.params}')
    position = scene.egoObject.position
    ratioo = scene.params["ratioo"]
    R = np.array([     # rotation matrix
      [0.9201568,  0.3915501],
      [-0.3915501, 0.9201568]
    ])
    location_random_2D = R @ np.array([position[0]*ratioo, position[1]*ratioo]) + np.array([291.85, -32627.15])  # adjust according to center of runway
    height = ((position[1]*ratioo - (-scene.params["real_lengthh"]/2)) / scene.params["real_lengthh"]) * (locations[0][1]-locations[3][1]) + locations[3][1] 
    location_random_3D = (location_random_2D[0], height, location_random_2D[1])
    # print(location_random_3D)

    client.setLocation(location_random_3D)
    sleep(SLEEP_TIME_SECONDS)

  # for location in locations:
  #   client.setLocation(location)
  #   sleep(SLEEP_TIME_SECONDS)