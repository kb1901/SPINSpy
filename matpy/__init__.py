# Initialization for package.
__author__ = "Ben Storer <bastorer@uwaterloo.ca>"
__date__   = "29th of April, 2015"

# Read in the defined functions. Not strictly necessary,
# but makes usage nicer. i.e. now we can use
# matpy.cheb(5) instead of matpy.cheb.cheb(5).
from cheb import cheb
from darkjet import darkjet
from FiniteDiff import FiniteDiff

# Define what happens when someone uses
# from matpy import *
__all__ = ["cheb", "darkjet", "FiniteDiff"]

