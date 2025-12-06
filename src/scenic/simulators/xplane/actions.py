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

class SetErrorAction(Action):
    def __init__(self, cmd):
        print(f"SetErrorAction initialized to send {cmd}")
        self.cmd = cmd

    def applyTo(self, obj, sim):
        """Set an error state in the simulation."""
        print(f"Setting error state in simulation")
        print(f"{sim.wrapper.client.sendDREF(self.cmd, 6)}")  # Example of sending a control command

class SendCOMMAction(Action):
    """
    This Action sends a COMM command to X-Plane.

    Args:
        command: The COMM command string to send
    """

    def __init__(self, command):
        print("SendCOMMAction initialized with command:", command)
        self.command = command

    def applyTo(self, obj, sim):
        """Send the COMM command to X-Plane."""
        print(f"Sending COMM command: {self.command}")
        sim.wrapper.client.sendCOMM(self.command)

class SetRecoverAction(Action):
    """
    This Action recovers the aircraft from a crashed state in X-Plane.
    """

    def __init__(self, recover_time = 15):
        self.recover_time = recover_time
        print(f"SetRecoverAction initialized with recover_time: {self.recover_time}")

    def applyTo(self, obj, sim):
        """Recover the aircraft from a crashed state."""
        sim.recoverCounter = self.recover_time
        sim.recovered = True

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
        sim.wrapper.setAutopilotMode(self.mode)
