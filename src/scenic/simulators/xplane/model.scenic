"""Scenic world model for the X-Plane simulator.

   In its current state, the model only supports the Beechcraft Baron 58 airplane
   and the LOWS R 15 airport.
"""

class Plane:
  """ Bounding box representing the Beechcraft Baron 58. 
  """
  position: (Range(-225, 851), Range(337, 350), Range(-33897, -31355))
