from enum import Enum

"""
Holds the information of the colors used in this program uses RGB values for colors
"""

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (211, 211, 211)
    RED = (255, 0, 255)
    GREEN = (0, 255, 0)
    ORANGE = (255,165,0)
    BLUE = (51, 255, 255)
    MAGENTA = (100, 0, 255)
    YELLOW = (255, 255, 0)