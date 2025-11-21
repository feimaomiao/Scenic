""" This script gets the corners of the runway for the LOWS R 15 airport runway assumping
    that the player is flying the Beechcraft Baron 58 aircraft.
"""
from time import sleep

from xpc import XPlaneConnect

X_DREF = "sim/flightmodel/position/local_x"
Y_DREF = "sim/flightmodel/position/local_y"
Z_DREF = "sim/flightmodel/position/local_z"
COORDS_DREFS = [X_DREF, Y_DREF, Z_DREF]

SLEEP_INTERVAL = 2

getCurrentPos = lambda : client.getDREFs(COORDS_DREFS)

def setOffset(dref, offset):
  print("Back to center of runway.")
  client.sendDREF(dref, client.getDREF(dref)[0] + offset)
  return

def resetPos(center):
  client.sendDREFs(COORDS_DREFS, [center[0][0], center[1][0], center[2][0]])

if __name__ == "__main__":
  client = XPlaneConnect()
  client.getDREF("sim/test/test_float")

  print("Current Location:")
  print(getCurrentPos())

  # CENTER = getCurrentPos()
  # print("Center of the runway:")
  # print(CENTER)
  # sleep(SLEEP_INTERVAL)

  # setOffset(X_DREF, -150)
  # setOffset(Z_DREF, 300)
  # print("Top of the runway:")
  # print(getCurrentPos())
  # sleep(SLEEP_INTERVAL)

  # resetPos(CENTER)