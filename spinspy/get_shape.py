from spinspy_classes import Grid

## Determine field shapes
## ------
def get_shape():

    grid_data = Grid()
    
    # Hard-coded for the time being
    grid_data.nd = 2#3
    
    grid_data.Nx = 128#3072
    grid_data.Ny = 128#192
    grid_data.Nz = 192

    return grid_data
## ------