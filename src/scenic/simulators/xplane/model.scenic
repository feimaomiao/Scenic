"""Scenic world model for the X-Plane simulator.

   In its current state, the model only supports the Beechcraft Baron 58 airplane
   and the LOWS R 15 airport.
"""
RUNWAY_CENTER = (-237, 338, -33869)
RUNWAY_LENGTH = (851 - -266) + 1
RUNWAY_WIDTH =  (351 - 337) + 1
RUNWAY_HEIGHT = (-31355 - -33897) + 1

workspace = Workspace(
  RectangularRegion(RUNWAY_CENTER, RUNWAY_LENGTH, RUNWAY_WIDTH, RUNWAY_HEIGHT, 'runway')
)
Runway = workspace

class Plane:
  """ Bounding box representing the Beechcraft Baron 58. 
  """
  position: (Range(-266, 851), Range(337, 350), Range(-33897, -31355))
  width: 10
  height: 10
  length: 10
  shape: BoxShape()
