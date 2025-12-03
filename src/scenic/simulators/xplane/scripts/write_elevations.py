"""Script that continuously writes current x, y, z coordinates to elevations.csv.
   Updates every 0.25 seconds.
"""
import csv
import time
from scenic.simulators.xplane.common import *

def write_elevations_csv(output_file='elevations.csv', update_interval=1.5):
    """
    Continuously write current aircraft position to CSV file.

    Args:
        output_file: Path to output CSV file (default: 'elevations.csv')
        update_interval: Time in seconds between updates (default: 0.25)
    """
    client = XPlaneWrapper()

    # Open file and write header
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x', 'y', 'z'])

    print(f"Writing coordinates to {output_file}. Press Ctrl+C to stop.")

    try:
        while True:
            # Get current position
            x, y, z = client.getPosition()

            # Append to CSV file
            with open(output_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([x, y, z])

            print(f"Wrote: x={x}, y={y}, z={z}")

            # Wait before next update
            time.sleep(update_interval)

    except KeyboardInterrupt:
        print(f"\nStopped writing to {output_file}")


if __name__ == "__main__":
    write_elevations_csv()
