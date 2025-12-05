try:
    from scenic.simulators.xplane.actions import *
except ModuleNotFoundError:
    pass    # ignore; error will be caught later if user attempts to run a simulation

behavior TeleportBehavior(targetPosition):
    """Behavior that teleports the ego to a specified position."""
    take TeleportAction(targetPosition)

behavior waitingBehavior():
    """Behavior that waits indefinitely."""
    while True:
        wait

behavior setFPMBehavior(board_code):
    if board_code != 430:
        raise ValueError("UnImplemented board code for flight plan setting!")
    """Behavior that sets the flight plan mode on a specified GPS board."""
    take SendCOMMAction("sim/GPS/g430n1_msg")
    take SendCOMMAction("sim/GPS/g430n1_proc")
    take SendCOMMAction("sim/GPS/g430n1_fpl")
    take SendCOMMAction("sim/GPS/g430n1_page_up")
    take SendCOMMAction("sim/GPS/g430n1_cursor")
    take SendCOMMAction("sim/GPS/g430n1_ent")
    take SendCOMMAction("sim/GPS/g430n1_cursor")
    take SendCOMMAction("sim/GPS/g430n1_ent")


behavior FlyRoute(startingpoint):
    # first the plane is teleported to the starting point
    take SetAutopilotAction(enabled=False)
    take TeleportAction(startingpoint)
    do setFPMBehavior(430)
    # then the plane is set to fly the route
    take SetAutopilotAction(enabled=True)
