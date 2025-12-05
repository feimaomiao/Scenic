import xpc
import time

def load_fms_plan_gps430():
    """Load a flight plan from the FMS plans directory into GPS 430"""
    
    with xpc.XPlaneConnect() as client:
        print("Opening GPS 430 Flight Plan page...")
        client.sendCOMM("sim/GPS/g430n1_msg")
        time.sleep(2)  # Wait for the GPS to process the command
        client.sendCOMM("sim/GPS/g430n1_proc")
        time.sleep(2)  # Wait for the GPS to process the command
        client.sendCOMM("sim/GPS/g430n1_fpl")
        time.sleep(2)  # Wait for the GPS to process the command
        client.sendCOMM("sim/GPS/g430n1_page_up")
        time.sleep(2)
        client.sendCOMM("sim/GPS/g430n1_cursor")
        time.sleep(2)
        client.sendCOMM("sim/GPS/g430n1_ent")

        

if __name__ == "__main__":
    load_fms_plan_gps430()