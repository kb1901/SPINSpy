# SPINSPY
#   This module contains functions that are
#   designed to handle SPINS-type outputs.
#   The provided functions are listed below,
#   along with basic usage information.

__author__ = "Ben Storer <bastorer@uwaterloo.ca>"
__date__   = "16th of December, 2014"

# Initialization file for package.
# Read in the defined functions. Not strictly necessary,
# but makes usage nicer. i.e. now we can use
# spinspy.grid() instead of spinspy.grid.grid().
from get_shape import get_shape
from grid import grid
from reader import reader
from spinspy_classes import Grid
from get_diagnostics import get_diagnostics

# Define what happens when someone uses
# from matpy import *
__all__ = ["get_shape", "grid", "reader", "spinspy_classes","get_diagnostics"]
