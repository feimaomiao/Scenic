import math
import time
import numpy as np

from xpc import XPlaneConnect
from pathlib import Path


def write_flight_plan(xplane_install_path: Path, flight_path: str, name: str):
  """ Write the flight plan to the X-Plane FMS directory."""
  fms_path = xplane_install_path / "Output" / "FMS plans"
  fms_path.mkdir(parents=True, exist_ok=True)
  print("Removeing old flight plans...")
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

  def setAutopilotMode(self, mode):
    self.client.sendDREF("sim/operation/prefs/ai_flies_aircraft", mode)

  def getCrashed(self):
    crashedInt = int(self.client.getDREF("sim/flightmodel2/misc/has_crashed")[0])
    crashed = crashedInt != 0

    print(f"Plane Crashed: {crashed}")
    return crashed