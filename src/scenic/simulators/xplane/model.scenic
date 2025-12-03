"""Scenic world model for the X-Plane simulator.
"""
import math

from scenic.simulators.xplane.simulator import XPlaneSimulator

POINTS = [
  (850, 350.7986755371094, -31372),                            # top left corner
  (808.9561157226562, 351.1387634277344, -31355.494140625),    # top right corner
  (-225.74005126953125, 337.68798828125, -33897.8203125),      # bottom left corner
  (-266.25006103515625, 337.9598083496094, -33882.296875),     # bottom right corner
  (291.85, 343.5, -32627.15)                                   # center of runway
]

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


  # Normalize width to 10 and scale height proportionally
  normalized_width = 10
  normalized_height = round((length / width) * normalized_width)
  return ((0, 0, 0), 0, normalized_width, normalized_height, length, width)

vec, orientation, norm_width, norm_height, real_length, real_width = points_to_normalized_rectangle(POINTS)

workspace = Workspace(RectangularRegion(vec,orientation, norm_width, norm_height, 'runway'))
Runway = workspace
ratio = real_width / norm_width

class Plane:
  """ Bounding box representing the Beechcraft Baron 58. 
  """
  # plane width = 11.53m
  # plane height = 2.97m
  # plane length = 9.09m
  width: 11.53 / ratio
  height: 2.97 / ratio
  length: 9.09 / ratio
  shape: BoxShape()

param ratioo = ratio
param real_lengthh = real_length
param real_widthh = real_width

simulator XPlaneSimulator()