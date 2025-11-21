""" This script gets the corners of the runway for the LOWS R 15 airport runway assumping
    that the player is flying the Beechcraft Baron 58 aircraft.
"""
from time import sleep

from xpc import XPlaneConnect

SLEEP_TIME_SECONDS = 2

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

  CENTER = client.getPosition()
  locations = [
    (851.549560546875, 350.7986755371094, -31377.404296875),   # top left corner
    (808.9561157226562, 351.1387634277344, -31355.494140625),  # top right corner
    (-225.74005126953125, 337.68798828125, -33897.8203125)     # bottom left corner
    (-266.25006103515625, 337.9598083496094, -33882.296875)    # bottom right corner
    CENTER
  ]

  for location in locations:
    client.setLocation(location)
    sleep(SLEEP_TIME_SECONDS)