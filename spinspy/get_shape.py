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