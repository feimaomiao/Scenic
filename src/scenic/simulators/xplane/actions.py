from scenic.core.simulators import * # imports the Action superclass
class TeleportAction(Action):
    """
    This Action teleports the aircraft to a specific (x, y, z) coordinate in X-Plane.

    Args:
        target_position: Either a tuple/list of (x, y, z) coordinates, or individual x, y, z values
    """

    def __init__(self, *args):
        print("TeleportAction initialized with args:", args)
        # Support both TeleportAction((x, y, z)) and TeleportAction(x, y, z)
        if len(args) == 1 and (isinstance(args[0], (tuple, list))):
            self.target_coord = args[0]
        elif len(args) == 3:
            self.target_coord = args
        else:
            raise ValueError("TeleportAction requires either a tuple (x, y, z) or three separate coordinates")

    def applyTo(self, obj, sim):
        """Teleport the aircraft to the target coordinates using X-Plane's wrapper."""
        print("Applying TeleportAction to target_coord:", self.target_coord)
        sim.wrapper.setLocation(self.target_coord)

class SetFPMAction(Action):
    """
    This Action sets the flight plan in X-Plane using a specified FMS file.

    Args:
        fms_file: Path to the FMS file to load
    """

    def __init__(self, board_code):
        print("SetFPMAction initialized")
        self.code = board_code

    def applyTo(self, obj, sim):
        """Set the flight plan in X-Plane using the provided FMS file."""
        print("Opening GPS 430 Flight Plan page...")
        if self.code == 430:
            sim.wrapper.g430_setflightplan()
        else:
            # If you're reading this and want to implement other board codes, check the following link
            # https://www.siminnovations.com/xplane/command/?name=sim%2FGPS&description=&submit=Search
            raise ValueError("Unsupported board code for flight plan setting, gotta implement it yourself!")
        


class SetAutopilotAction(Action):
    """
    This Action sets the autopilot in X-Plane.

    Args:
        autopilot_mode: The mode to set the autopilot to
    """

    def __init__(self, enabled=True):
        print("SetAutopilotAction initialized")
        self.mode = enabled

    def applyTo(self, obj, sim):
        """Set the autopilot mode in X-Plane."""
        print(f"Setting autopilot mode to: {self.mode}")
        # Implement the logic to set the autopilot mode using X-Plane's wrapper
        # This is a placeholder; actual implementation will depend on X-Plane's API
        sim.wrapper.setAutopilotMode(self.mode)
