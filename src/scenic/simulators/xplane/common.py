import math
import time
import numpy as np

from xpc import XPlaneConnect

SLEEP_TIME_SECONDS = 1

class XPlaneWrapper():
  X_DREF = "sim/flightmodel/position/local_x"
  Y_DREF = "sim/flightmodel/position/local_y"
  Z_DREF = "sim/flightmodel/position/local_z"
  COORDS_DREFS = [X_DREF, Y_DREF, Z_DREF]

  def __init__(self):
    self.client = XPlaneConnect(timeout=10000)
    return
  
  def getTestFloat(self):
    try:
      return self.client.getDREF("sim/test/test_float")
    except:
      raise RuntimeError("Failed to establish connection to XPlane.")

  def getPosition(self):
    position = self.client.getDREFs(self.COORDS_DREFS)
    return tuple([int(coord[0]) for coord in position])

  def setOffset(self, dref, offset):
    self.client.sendDREF(dref, self.client.getDREF(dref)[0] + offset)
    return

  def setLocation(self, location):
    self.client.sendDREFs(self.COORDS_DREFS, [location[0], location[1], location[2]])
    return
  
  def g430_setflightplan(self):
    self.client.sendCOMM("sim/GPS/g430n1_msg")
    time.sleep(0.5)  # Wait for the GPS to process the command
    self.client.sendCOMM("sim/GPS/g430n1_proc")
    time.sleep(0.5)  # Wait for the GPS to process the command
    self.client.sendCOMM("sim/GPS/g430n1_fpl")
    time.sleep(0.5)  # Wait for the GPS to process the command
    self.client.sendCOMM("sim/GPS/g430n1_page_up")
    time.sleep(0.5)
    self.client.sendCOMM("sim/GPS/g430n1_cursor")
    time.sleep(0.5)
    self.client.sendCOMM("sim/GPS/g430n1_ent")
    print("Flight plan set on GPS 430.")

  def setAutopilotMode(self, mode):
    self.client.sendDREF("sim/operation/prefs/ai_flies_aircraft", mode)

  def getCrashed(self):
    crashedInt = int(self.client.getDREF("sim/flightmodel2/misc/has_crashed")[0])
    crashed = crashedInt != 0

    print(f"Plane Crashed: {crashed}")
    return crashed