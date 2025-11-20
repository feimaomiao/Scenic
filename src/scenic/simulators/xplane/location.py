""" This script gets the corners of the runway for the LOWS R 15 airport runway assumping
    that the player is flying the Beechcraft Baron 58 aircraft.
"""
from time import sleep

from xpc import XPlaneConnect

LAT = 0
LON = 1
ALT = 2
PITCH = 3
ROLL = 4
YAW = 5
GEAR = 6
FIELDS = ["Lat", "Lon", "Alt", "Pitch", "Roll", "Yaw", "Gear"]

SLEEP_INTERVAL = 2

def printPosition(position):
  assert(len(position) == len(FIELDS))

  for i in range(0, len(position)):
    print(f"{FIELDS[i]}: {position[i]}")
  
  print()
  return

def setOffset(client, lat, lon, alt):
  newPosition = list(client.getPOSI())
  
  newPosition[LAT] += lat
  newPosition[LON] += lon
  newPosition[ALT] += alt

  client.sendPOSI(newPosition)
  return newPosition

def resetPosition(client, center):
  print("Back to center.")
  client.sendPOSI(center)
  sleep(SLEEP_INTERVAL)
  return

if __name__ == "__main__":
  client = XPlaneConnect()
  client.getDREF("sim/test/test_float")

  print("Center of the runway:")
  position = client.getPOSI()
  printPosition(position)
  sleep(SLEEP_INTERVAL)

  CENTER = position

  # print("Left corner of runway:")
  # setPosition(client, LON, position[LON] + 0.0004)
  # printPosition(position)
  # sleep(SLEEP_INTERVAL)

  # print("Left side of runway:")
  # setPosition(client, LON, position[LON] + 0.0004)
  # printPosition(position)
  # sleep(SLEEP_INTERVAL)

  # resetPosition(client, CENTER)

  # print("Right side of runway:")
  # setPosition(client, LON, position[LON] - 0.0004)
  # printPosition(position)
  # sleep(SLEEP_INTERVAL)

  # resetPosition(client, CENTER)

  print("Top of runway:")
  newPosition = setOffset(client, 0, 0.005, 0)
  printPosition(newPosition)
  sleep(SLEEP_INTERVAL)

  resetPosition(client, CENTER)