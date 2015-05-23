import numpy as np
import spinspy as spy

# need to test on 2D and if grid style is full

## Determine simulation parameters and make grid
## Purpose:
##     - Read spins.conf if it exists
##     - Read the grid
##     - Add other grid parameters (such as grid spacing) into parameters object
##
## Usage:
##     x,y[,z],params = spinspy.get_paramgrid()
## ------
def get_paramgrid(style='vector'):
    # read parameters and grid
    params = spy.get_params()

    # Parse the grid based on which dimensions are used
    if params.nd == 3:
        x,y,z = spy.get_grid(style=style)
    elif params.nd == 2:
        if params.Nz == 1:
            x,y = spy.get_grid(style=style)
        if params.Ny == 1:
            x,z = spy.get_grid(style=style)
        if params.Nx == 1:
            y,z = spy.get_grid(style=style)
    Nz = params.Nz

    # Find other grid parameters
    if params.Nx > 1:
        dx = x[1] - x[0]
        params.dx = dx
        params.xlim = [x[0],x[-1]]
        params.Lx = np.abs(x[-1]-x[0])
    if params.Ny > 1:
        dy = y[1] - y[0]
        params.dy = dy
        params.ylim = [y[0],y[-1]]
        params.Ly = np.abs(y[-1]-y[0])
    if params.Nz > 1:
        params.zlim = [z[0],z[-1]]
        params.Lz = np.abs(z[-1]-z[0])

    # Print dimensionality
    # BS: Do we need this?
    if params.nd == 3:
        print('Data is 3 dimensional.')
    elif params.nd == 2:
        print('Data is 2 dimensional.')

    # check for vertical expansion style
    if np.abs((z[Nz/2]-z[Nz/2-1])/(z[1]-z[0])) > 2:
        print('Chebyshev grid in z.')
        # DD: define clenshaw curtis weights here?
        # BS: if it's easy to do, sure?
    else:
        print('Linear grid in z.')
        dz = z[1]-z[0]
        params.dz = dz

    return gd, params
