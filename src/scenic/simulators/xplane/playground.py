try:
  from xpc import XPlaneConnect
except ImportError as exception:
  raise RuntimeError('The X-Plane interface requires XPlaneConnect.') from exception


POSI = ["Lat", "Lon", "Alt", "Pitch", "Roll", "Yaw", "Gear"]

if __name__ == "__main__":
  with XPlaneConnect() as client:
    try:
      position = client.getPOSI()
      control = client.getCTRL()

      print(position)

    except:
      raise RuntimeError("Failed to establish connection to XPlane.")