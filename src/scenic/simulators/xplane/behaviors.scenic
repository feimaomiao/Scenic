import math
import itertools 

from scenic.syntax.veneer import verbosePrint
try:
    from scenic.simulators.xplane.actions import *
except ModuleNotFoundError:
    pass    # ignore; error will be caught later if user attempts to run a simulation

behavior waitingBehavior(count = 0, indefinite = False):
    """Behavior that waits indefinitely."""
    while count > 0:
        wait
        if not indefinite:
            count -= 1

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
    do waitingBehavior(3)
    # first the plane is teleported to the starting point
    take SendCOMMAction("sim/operation/reset_flight")
    take SetAutopilotAction(enabled=False)
    # take TeleportAction(startingpoint)
    do setFPMBehavior(430)
    # then the plane is set to fly the route
    take SetAutopilotAction(enabled=True)
    verbosePrint("Ready for takeoff")
    do waitingBehavior(1, indefinite=True)

behavior FailureBehavior(errors, recovery):
    """Behavior that sets an failed state in the simulation, wait for some time, then try to recovers."""
    verbosePrint("Starting Failure Behavior with errors:", errors)
    take SetAutopilotAction(enabled=False)
    for e in errors:
        take SetErrorAction(e)
    do waitingBehavior(recovery)
    take SetAutopilotAction(enabled=True)
    take SetRecoverAction(recovery)
    do waitingBehavior(recovery)
    
    
behavior FlyWithRandomFailureAfterDistance(startingpoint, distance, errors,error_count, recovery):
    verbosePrint("Starting Fly with the following parameters:")
    verbosePrint(f"Starting point: {startingpoint}")
    verbosePrint(f"Distance to failure: {distance}")
    verbosePrint(f"Errors: {errors}")
    verbosePrint(f"Recovery time: {recovery} seconds")
    try:
        do FlyRoute(startingpoint)
    interrupt when distance from ego to (0,0,0) > distance:
        verbosePrint(f"Simulating errors! {distance from ego to (0,0,0)}")
        do FailureBehavior()
        terminate

behavior FlyErrorAtHeight(startingpoint, height, errors, recovery):
    # eval_error_count = DiscreteRange(1, len(errors))
    error_count = Discrete(
    {i: len(errors)-i + 1 for i in range(1, len(errors)+1)}
    )
    eval_errors = Uniform(*itertools.combinations(errors, error_count))
    verbosePrint("Starting Fly with the following parameters:")
    verbosePrint(f"Starting point: {startingpoint}")
    verbosePrint(f"Height to failure: {height}")
    verbosePrint(f"Errors: {eval_errors}")
    verbosePrint(f"Error count: {error_count}")
    verbosePrint(f"Recovery time: {recovery} seconds")
    try:
        do FlyRoute(startingpoint)
    interrupt when ego.position.z > height:
        verbosePrint(f"Simulating errors! Current height: {ego.position.z}")
        do FailureBehavior(eval_errors, recovery)
        terminate
    
