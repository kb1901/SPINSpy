from reader import reader
from get_shape import get_shape

## Read in the grid
## ------
def grid(type='vector'):
    # This reads in the grid and produces a dictionary
    # that contains x, y, z, dx, dy, dz, Lx, Lx,
    # Lz, Nx, Ny, and Nz.
    
    grid_data = get_shape()
    
    if grid_data.nd == 2:
        if type == 'vector':
            x = reader('x', [0,-1],0)
            y = reader('y', 0,[0,-1])
        elif type == 'full':
            x = reader('x', [0,-1],[0,-1])
            y = reader('y', [0,-1],[0,-1])
    if grid_data.nd == 3:
        if type == 'vector':
            x = reader('x', [0,-1],0,0)
            y = reader('y', 0,[0,-1],0)
            z = reader('z', 0,0,[0,-1])
        elif type == 'full':
            x = reader('x', [0,-1],[0,-1],[0,-1])
            y = reader('y', [0,-1],[0,-1],[0,-1])
            z = reader('z', [0,-1],[0,-1],[0,-1])

    if grid_data.nd == 2:
        return x,y
    elif grid_data.nd == 3:
        return x,y,z
## ------