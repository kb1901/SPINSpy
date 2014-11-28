# Initialization file for package. Does nothing.

# Read in the defined functions. Not strictly necessary,
# but makes usage nicer. i.e. now we can use
# matpy.cheb(5) instead of matpy.cheb.cheb(5).
from get_shape import get_shape
from get_data import get_data
from grid import grid
from reader import reader
from spinspy_classes import Grid

# Define what happens when someone uses
# from matpy import *
__all__ = ["get_data", "get_shape", "grid", "reader", "spinspy_classes"]