try:
    from scenic.simulators.xplane.actions import *
except ModuleNotFoundError:
    pass    # ignore; error will be caught later if user attempts to run a simulation

behavior TeleportBehavior(targetPosition):
    """Behavior that teleports the ego to a specified position."""
    take TeleportAction(targetPosition)
    while True:
        wait

behavior waitingBehavior():
    """Behavior that waits indefinitely."""
    while True:
        wait

behavior FlyRoute(startingpoint):
    # first the plane is teleported to the starting point
    take TeleportAction(startingpoint)
    take SetFPMAction(430)
    take SetAutopilotAction(enabled=True)
