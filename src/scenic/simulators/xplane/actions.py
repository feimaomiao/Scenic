from scenic.core.simulators import * # imports the Action superclass
from scenic.syntax.veneer import verbosePrint
class TeleportAction(Action):
    """
    This Action teleports the aircraft to a specific (x, y, z) coordinate in X-Plane.

    Args:
        target_position: Either a tuple/list of (x, y, z) coordinates, or individual x, y, z values
    """

    def __init__(self, *args):
        verbosePrint("TeleportAction initialized with args:", args, level=3)
        # Support both TeleportAction((x, y, z)) and TeleportAction(x, y, z)
        if len(args) == 1 and (isinstance(args[0], (tuple, list))):
            self.target_coord = args[0]
        elif len(args) == 3:
            self.target_coord = args
        else:
            raise ValueError("TeleportAction requires either a tuple (x, y, z) or three separate coordinates")

    def applyTo(self, obj, sim):
        """Teleport the aircraft to the target coordinates using X-Plane's wrapper."""
        verbosePrint("Applying TeleportAction to target_coord:", self.target_coord, level=3)
        sim.wrapper.setLocation(self.target_coord)

class SetErrorAction(Action):
    def __init__(self, cmd):
        self.cmd = cmd

    def applyTo(self, obj, sim):
        """Set an error state in the simulation."""
        sim.wrapper.client.sendDREF(self.cmd, 6)

class SendCOMMAction(Action):
    """
    This Action sends a COMM command to X-Plane.

    Args:
        command: The COMM command string to send
    """

    def __init__(self, command):
        self.command = command

    def applyTo(self, obj, sim):
        """Send the COMM command to X-Plane."""
        sim.wrapper.client.sendCOMM(self.command)

class SetRecoverAction(Action):
    """
    This Action recovers the aircraft from a crashed state in X-Plane.
    """

    def __init__(self, recover_time = 15):
        self.recover_time = recover_time

    def applyTo(self, obj, sim):
        """Recover the aircraft from a crashed state."""
        verbosePrint("Starting recover procedure, with recover time:", self.recover_time, level=3)
        sim.recoverCounter = self.recover_time
        sim.recovered = True

class SetAutopilotAction(Action):
    """
    This Action sets the autopilot in X-Plane.

    Args:
        autopilot_mode: The mode to set the autopilot to
    """

    def __init__(self, enabled=True):
        self.mode = enabled

    def applyTo(self, obj, sim):
        """Set the autopilot mode in X-Plane."""
        # Implement the logic to set the autopilot mode using X-Plane's wrapper
        sim.wrapper.setAutopilotMode(self.mode)
