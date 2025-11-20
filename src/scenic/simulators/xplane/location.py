try:
  from xpc import XPlaneConnect
except ImportError as exception:
  raise RuntimeError('The X-Plane interface requires XPlaneConnect.') from exception

def printPosition(client):
  fields = ["Lat", "Lon", "Alt", "Pitch", "Roll", "Yaw", "Gear"]

  position = client.getPOSI()
  for i in range(0, len(position)):
    print(f"{fields[i]}: {position[i]}")
  
  print()
  return

if __name__ == "__main__":
  client = XPlaneConnect()

  print(f"Position at the center of the runway:")
  printPosition(client)