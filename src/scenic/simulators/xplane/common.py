import math
import time
import numpy as np

from xpc import XPlaneConnect
from pathlib import Path

TIMEOUT = 1000000000

def write_flight_plan(xplane_install_path: Path, flight_path: str, name: str):
  """ Write the flight plan to the X-Plane FMS directory."""
  fms_path = xplane_install_path / "Output" / "FMS plans"
  fms_path.mkdir(parents=True, exist_ok=True)
  print("Removing old flight plans...")
  for item in fms_path.iterdir():
      if item.is_file():
          item.unlink()
  print("Writing new flight plan...")
  with open(fms_path / f"{name}.fms", "w") as f:
      f.write(flight_path)
  pass

class XPlaneWrapper():
  X_DREF = "sim/flightmodel/position/local_x"
  Y_DREF = "sim/flightmodel/position/local_y"
  Z_DREF = "sim/flightmodel/position/local_z"
  COORDS_DREFS = [X_DREF, Y_DREF, Z_DREF]

  def __init__(self):
    self.client = XPlaneConnect(timeout=TIMEOUT)
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

  def setAutopilotMode(self, mode):
    self.client.sendDREF("sim/operation/prefs/ai_flies_aircraft", mode)
    return

  def sendCTRL(self, command):
    self.client.sendCTRL(command)
    return

  def getCrashed(self):
    crashedInt = int(self.client.getDREF("sim/flightmodel2/misc/has_crashed")[0])
    crashed = crashedInt != 0

    print(f"Plane Crashed: {crashed}")
    return crashed
  
  def setRain(self, rainpercent):
    '''[0.0 - 1.0] The percentage of rain falling.'''
    self.client.sendDREF("sim/weather/region/rain_percent", rainpercent)
    return
  
  def setWeatherChange(self, change_mode):
    '''How the weather is changing. 0 = Rapidly Improving, 1 = Improving, 2 = Gradually Improving, 
    3 = Static, 4 = Gradually Deteriorating, 5 = Deteriorating, 6 = Rapidly Deteriorating, 7 = Using Real Weather'''

    self.client.sendDREF("sim/weather/region/change_mode", change_mode)
    return
  
  def setCloudType(self, cloud_type):
    '''Blended cloud types per layer. 0 = Cirrus, 1 = Stratus, 2 = Cumulus, 
    3 = Cumulo-nimbus. Intermediate values are to be expected.'''
    self.client.sendDREF("sim/weather/region/cloud_type", cloud_type)
    return
