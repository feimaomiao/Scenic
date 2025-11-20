from xpc import XPlaneConnect

LAT = 0
LON = 1
ALT = 2
PITCH = 3
ROLL = 4
YAW = 5
GEAR = 6
FIELDS = [i for i in range(LAT, GEAR + 1)]

def printPosition(position):
  assert(len(position) == len(FIELDS))

  for i in range(0, len(position)):
    print(f"{FIELDS[i]}: {position[i]}")
  
  print()
  return

def setPosition(client, field, newValue):
  position = list(client.getPOSI())
  position[field] = newValue
  client.sendPOSI(position)
  return

if __name__ == "__main__":
  client = XPlaneConnect()

  print(f"Position at the center of the runway:")
  position = client.getPOSI()
  printPosition(position)

  setPosition(client, LAT, position[LAT] + 100)
  printPosition(position)