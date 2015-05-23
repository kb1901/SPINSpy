import numpy as np
import spinspy as spy

## Determine simulation parameters and make grid
## Purpose:
##     - Read spins.conf if it exists
##     - Read the grid
##     - Add other grid parameters (such as grid spacing) into parameters object
##
## Usage:
##     paramgrid = spinspy.get_paramgrid()
## ------

# need to test on 2D and if grid style is full

def get_paramgrid(style='vector'):
    # read parameters and grid
    params = spy.get_params()
    gd = spy.get_grid(style=style)    # gd = x,[y],z
    x = gd[0]
    z = gd[-1]
    Nz = params.Nz

    # find other grid parameters
    dx = x[1]-x[0]
    params.dx = dx
    #params.Lx = params.Nx*dx   # do I need this?
    if params.nd == 3:
        y = gd[1]
        dy = y[1]-y[0]
        params.dy = dy
        #gd.Ly = gd.Ny*dy
        print('Data is 3 dimensional.')
    elif params.nd == 2:
        print('Data is 2 dimensional.')

    # check for vertical expansion style
    if np.abs((z[Nz/2]-z[Nz/2-1])/(z[1]-z[0])) > 2:
        print('Chebyshev grid in z.')
        # define clenshaw curtis weights here?
    else:
        print('Linear grid in z.')
        dz = z[1]-z[0]
        params.dz = dz
        #gd.Lz = gd.Nz*dz

    return gd, params
