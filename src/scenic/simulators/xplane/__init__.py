"""Scenic world model for the X-Plane flight simulator.

See the `VerifAI distribution`_ for examples of how to use Scenic with X-Plane.

.. _VerifAI distribution: https://github.com/BerkeleyLearnVerify/VerifAI
"""

xpc = None
try:
  from xpc import XPlaneConnect
except ImportError:
  raise RuntimeError('The X-Plane interface requires XPlaneConnect.')

if xpc:
  from .simulator import XPlaneSimulator

del xpc