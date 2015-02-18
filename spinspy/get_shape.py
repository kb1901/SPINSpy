from spinspy_classes import Grid
import os
from spinspy import local_data

## Determine simulation parameters
## Purpose:
##     If spins.conf exists
##         parse spins.conf
##     Else
##         Use hard-coded values
##
## Usage:
##     data = spinspy.get_shape()
##
##     data.display() prints a summary
##                    of known values
## ------
def get_shape():

    grid_data = Grid()
    
    # Check if a spins.conf file exists,
    # if it does, parse it.
    conf_path = '{0:s}spins.conf'.format(local_data.prefix)
    if os.path.isfile(conf_path):
    
        grid_data = spinsconf_parser(grid_data)
    
    else:
        
        # Hard-coded back-up
        grid_data.nd = 3
    
        grid_data.Nx = 3072
        grid_data.Ny = 192
        grid_data.Nz = 192

    return grid_data
## ------


## Parser for spins.conf
## ------
def spinsconf_parser(grid_data):
    # Open the file for reading only.
    conf_path = '{0:s}spins.conf'.format(local_data.prefix)
    f = open(conf_path, 'r')

    # Loop through each line, parsing as we go.
    # Each line is assumed to be of the form
    # <str> = ## \n
    for line in f:
        # Find the lenght of the variable name
        var_len = 0
        line_len = len(line)
        for char in line:
            if char == '=':
                break
            else:
                var_len = var_len + 1
        # strip removes any leading and trailing whitespace
        var = line[0:var_len].strip()
        try:
            val = float(line[var_len+1:line_len-2].strip())
        except:
            val = line[var_len+1:line_len].strip()
    
        setattr(grid_data, var, val)

    # Close the file.
    f.close()

    # Double check that Nx,Ny,Nz have been assigned. If not, make them 1.
    if not(hasattr(grid_data,'Nx')):
        setattr(grid_data,'Nx',1)
    if not(hasattr(grid_data,'Ny')):
        setattr(grid_data,'Ny',1)
    if not(hasattr(grid_data,'Nz')):
        setattr(grid_data,'Nz',1)

    grid_data.Nx = int(grid_data.Nx)
    grid_data.Ny = int(grid_data.Ny)
    grid_data.Nz = int(grid_data.Nz)

    # Determine the number of dimensions
    # We're going to assume you aren't doing
    # a 1D simulation, so if any dimension
    # is a singleton, then it's a 2D simulation.
    if ((grid_data.Nx == 1) |
        (grid_data.Ny == 1) |
        (grid_data.Nz == 1)):
    
        grid_data.nd = 2
    
        # Also, Nz should be 1, not Ny
        if grid_data.Ny == 1:
            grid_data.Ny = grid_data.Nz
            grid_data.Nz = 1
    else:
        grid_data.nd = 3
    
    # Convert min_x,y,z to x,y,zlim
    for dim in ['x', 'y', 'z']:
        if (hasattr(grid_data, 'min_'+dim) &\
            hasattr(grid_data, 'L'+dim)):
            setattr(grid_data,dim+'lim',\
                    [getattr(grid_data,'min_'+dim),\
                     getattr(grid_data,'min_'+dim) + \
                     getattr(grid_data,'L'+dim)])

    return grid_data
## ------
