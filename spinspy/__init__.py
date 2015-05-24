# SPINSPY
#   This module contains functions that are
#   designed to handle SPINS-type outputs.
#   The provided functions are listed below,
#   along with basic usage information.

__author__ = "Ben Storer <bastorer@uwaterloo.ca>"
__date__   = "22th of May, 2015"

# Create a Params instance for storing information
from spinspy_classes import Params
local_data = Params()
local_data.path = './'
local_data.grid_path = ''
local_data.conf_path = ''

# Initialization file for package.
# Read in the defined functions. Not strictly necessary,
# but makes usage nicer. i.e. now we can use
# spinspy.grid() instead of spinspy.grid.grid().
from get_params import get_params
from get_grid import get_grid
from get_paramgrid import get_paramgrid
from reader import reader
from get_diagnostics import get_diagnostics
from set_path import set_path
from plot2d import plot2d
from nearestindex import nearestindex

# Define what happens when someone uses
# from matpy import *
__all__ = ["spinspy_classes", "get_params", "get_grid", "get_paramgrid", "reader", "get_diagnostics", "set_path","plot2d", "nearestindex"]
