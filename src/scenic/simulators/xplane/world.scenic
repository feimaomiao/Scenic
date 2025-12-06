from scenic.simulators.xplane.common import Workspace, RectangularRegion
import math

def points_to_workspace(top_left, top_right, bottom_left, bottom_right):
    """
    Converts 4 separate 3D points to normalized width and length dimensions.

    This function extracts the x and z coordinates from a set of points (ignoring y),
    then calculates the distances between adjacent corners to determine the rectangle's
    dimensions.

    Args:
        top_left: Top-left corner point as a tuple/list of (x, y, z) coordinates.
        top_right: Top-right corner point as a tuple/list of (x, y, z) coordinates.
        bottom_left: Bottom-left corner point as a tuple/list of (x, y, z) coordinates.
        bottom_right: Bottom-right corner point as a tuple/list of (x, y, z) coordinates.

    Returns:
        tuple: A tuple of (width, length) where width is the smaller dimension
            and length is the larger dimension of the rectangle.

    Raises:
        IndexError: If any point does not contain at least 2 coordinates.
        TypeError: If points cannot be indexed or converted to numeric values.
    """
    # Distance between top-left and top-right gives one dimension
    dx1 = top_right[0] - top_left[0]
    dz1 = top_right[2] - top_left[2]
    edge1_length = math.sqrt(dx1**2 + dz1**2)

    # Distance between top-left and bottom-left gives other dimension
    dx2 = bottom_left[0] - top_left[0]
    dz2 = bottom_left[2] - top_left[2]
    edge2_length = math.sqrt(dx2**2 + dz2**2)

    # Determine width and length (width is typically the smaller dimension)
    width = min(edge1_length, edge2_length)
    length = max(edge1_length, edge2_length)


    param runway_length = length
    param runway_width = width
    return Workspace(RectangularRegion((0,0,0), 0, width, length, 'runway'))

