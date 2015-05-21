# SPINSPY
#   This module contains functions that are
#   designed to handle SPINS-type outputs.
#   The provided functions are listed below,
#   along with basic usage information.

__author__ = "Ben Storer <bastorer@uwaterloo.ca>"
__date__   = "29th of April, 2015"

# Create a grid Grid instance for storing information
from spinspy_classes import Grid
local_data = Grid()
local_data.prefix = ''

# Initialization file for package.
# Read in the defined functions. Not strictly necessary,
# but makes usage nicer. i.e. now we can use
# spinspy.grid() instead of spinspy.grid.grid().
from get_shape import get_shape
from grid import grid
from reader import reader
from get_diagnostics import get_diagnostics
from set_prefix import set_prefix
from grid_diagnostic  import grid_diagnostic

# Define what happens when someone uses
# from matpy import *
__all__ = ["get_shape", "grid", "reader", "spinspy_classes","get_diagnostics","grid_diagnostic"]
