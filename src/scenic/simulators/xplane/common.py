"""
   In its current state, the model only supports the Beechcraft Baron 58 airplane
   and the LOWS R 15 airport.
"""
import math

RUNWAY_CENTER = (-237, 338, -33869)
RUNWAY_LENGTH = (851 - -266) + 1
RUNWAY_WIDTH =  (351 - 337) + 1
RUNWAY_HEIGHT = (-31355 - -33897) + 1

POINTS = [
  (850, 350.7986755371094, -31372),                            # top left corner
  (808.9561157226562, 351.1387634277344, -31355.494140625),    # top right corner
  (-225.74005126953125, 337.68798828125, -33897.8203125),      # bottom left corner
  (-266.25006103515625, 337.9598083496094, -33882.296875),     # bottom right corner
  (291.85, 343.5, -32627.15)                                   # center of runway
]
