from spinspy_classes import Grid

## Determine field shapes
## ------
def get_shape():

    grid_data = Grid()
    
    # Hard-coded for the time being
    grid_data.nd = 3
    
    grid_data.Nx = 3072
    grid_data.Ny = 192
    grid_data.Nz = 192

    return grid_data
## ------

## Determine grid info
## ------
def get_data():
    
    grid_data = get_shape()
    
    if grid_data.nd >= 1:
        x = reader('x',[0,1,-1],0,0)
        grid_data.xlim = x[[0,2]]
        grid_data.Lx   = x[2] - x[0]
    if grid_data.nd >= 2:
        y = reader('y',0,[0,1,-1],0)
        grid_data.ylim = y[[0,2]]
        grid_data.Ly   = y[2] - y[0]
    if grid_data.nd >= 3:
        z = reader('z',0,0,[0,1,-1])
        grid_data.zlim = z[[0,2]]
        grid_data.Lz   = z[2] - z[0]
    
    return grid_data
## ------