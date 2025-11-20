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

if __name__ == "__main__":
  client = XPlaneConnect()
  client.getDREF("sim/test/test_float")

  print("Center of the runway:")
  coords = client.getDREFs(COORDS_DREFS)
  print(coords)

  CENTER = coords