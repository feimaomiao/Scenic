""" This script gets the corners of the runway for the LOWS R 15 airport runway assumping
    that the player is flying the Beechcraft Baron 58 aircraft.
"""
from time import sleep
import numpy as np
import argparse
from xpc import XPlaneConnect
from scenic.simulators.xplane.common import *

from scenic import scenarioFromFile

SLEEP_TIME_SECONDS = 3
POINTS = [
    (850, 350.7986755371094, -31372),                            # top left corner
    (808.9561157226562, 351.1387634277344, -31355.494140625),    # top right corner
    (-225.74005126953125, 337.68798828125, -33897.8203125),      # bottom left corner
    (-266.25006103515625, 337.9598083496094, -33882.296875),     # bottom right corner
    (291.85, 343.5, -32627.15)                                   # center of runway
]
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