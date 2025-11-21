""" This script gets the corners of the runway for the LOWS R 15 airport runway assumping
    that the player is flying the Beechcraft Baron 58 aircraft.
"""
from time import sleep

from xpc import XPlaneConnect

X_DREF = "sim/flightmodel/position/local_x"
Y_DREF = "sim/flightmodel/position/local_y"
Z_DREF = "sim/flightmodel/position/local_z"
COORDS_DREFS = [X_DREF, Y_DREF, Z_DREF]

SLEEP_TIME_SECONDS = 2

class XPlaneWrapper():

  def __init__(self):
    self.client = XPlaneConnect()
    return

  def getPosition(self):
    position = self.client.getDREFs(COORDS_DREFS)
    return (position[0], position[1], position[2])

  def setOffset(self, dref, offset):
    self.client.sendDREF(dref, self.client.getDREF(dref)[0] + offset)
    return

  def setLocation(self, location):
    self.client.sendDREFs(COORDS_DREFS, [location[0], location[1], location[2]])
    return


if __name__ == "__main__":
  client = XPlaneWrapper()

  locations = [
    (851.549560546875, 350.7986755371094, -31377.404296875),  # top left corner
    (808.9561157226562, 351.1387634277344, -31355.494140625),  # top right corner
    client.getPosition()
  ]

  for location in locations:
    client.setLocation(location)
    sleep(SLEEP_TIME_SECONDS)