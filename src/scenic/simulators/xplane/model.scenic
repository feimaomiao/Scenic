"""Scenic world model for the X-Plane simulator.
"""
from scenic.simulators.xplane.common import *
from scenic.simulators.xplane.simulator import XPlaneSimulator

def points_to_normalized_rectangle(points):
  """Convert four corner points to a normalized rectangle.

  Args:
      points: List of four (x, y, z) tuples representing corners of a rectangle.
              The y coordinate is ignored (treated as height).

  Returns:
      A tuple of (left_bottom_x, left_bottom_z, normalized_width, normalized_height) where:
      - left_bottom_x, left_bottom_z: Bottom-left corner of the rectangle
      - normalized_width: Width normalized to 10
      - normalized_height: Height as a ratio of width (scaled proportionally)
  """
  # Extract x and z coordinates (ignoring y)
  coords = [(p[0], p[2]) for p in points]

  # Compute distances between adjacent corners to find width and length
  # Assuming points are ordered as: top-left, top-right, bottom-left, bottom-right
  # Distance between top-left (0) and top-right (1) gives one dimension
  dx1 = coords[1][0] - coords[0][0]
  dz1 = coords[1][1] - coords[0][1]
  edge1_length = math.sqrt(dx1**2 + dz1**2)

  # Distance between top-left (0) and bottom-left (2) gives other dimension
  dx2 = coords[2][0] - coords[0][0]
  dz2 = coords[2][1] - coords[0][1]
  edge2_length = math.sqrt(dx2**2 + dz2**2)

  # Determine width and length (width is typically the smaller dimension)
  width = min(edge1_length, edge2_length)
  length = max(edge1_length, edge2_length)


  return (width, length)

width, length= points_to_normalized_rectangle(POINTS)

workspace = Workspace(RectangularRegion((0,0,0), 0, width, length, 'runway'))
Runway = workspace

class Plane:
  """ Bounding box representing the Beechcraft Baron 58. 
  """
  # plane width = 11.53m
  # plane height = 2.97m
  # plane length = 9.09m
  width: 11.53 
  height: 2.97 
  length: 9.09 
  shape: BoxShape()

param runway_length = length
param runway_width = width

simulator XPlaneSimulator()