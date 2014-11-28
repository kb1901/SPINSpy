## Read in the grid
## ------
def grid(type='vector'):
    # This reads in the grid and produces a dictionary
    # that contains x, y, z, dx, dy, dz, Lx, Lx,
    # Lz, Nx, Ny, and Nz.
    
    if type == 'vector':
        x = reader('x', [0,-1],0,0)
        y = reader('y', 0,[0,-1],0)
        z = reader('z', 0,0,[0,-1])
    elif type == 'full':
        x = reader('x', [0,-1],[0,-1],[0,-1])
        y = reader('y', [0,-1],[0,-1],[0,-1])
        z = reader('z', [0,-1],[0,-1],[0,-1])

    return x,y,z
## ------