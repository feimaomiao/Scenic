try:
  from xpc import XPlaneConnect
except ImportError as exception:
  raise RuntimeError('The X-Plane interface requires XPlaneConnect.') from exception

if __name__ == "__main__":
  with XPlaneConnect() as client:
    try:
      print(client.getPOSI())
      print(client.getCTRL())

    except:
      raise RuntimeError("Failed to establish connection to XPlane.")