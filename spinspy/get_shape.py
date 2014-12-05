from spinspy_classes import Grid
import os

## Determine field shapes
## ------
def get_shape():

    grid_data = Grid()
    
    # Check if a spins.conf file exists,
    # if it does, parse it.
    if os.path.isfile('spins.conf'):
    
        # Open the file for reading only.
        f = open('spins.conf', 'r')
        
        # Loop through each line, parsing as we go.
        # Each line is assumed to be of the form
        # <str> = ## \n
        for line in f:
            # Find the lenght of the variable name
            # The -1 accounts for the space between the name
            # and the '='
            var_len = -1
            line_len = len(line)
            for char in line:
                if char == '=':
                    break
                else:
                    var_len = var_len + 1
            var = line[0:var_len]
            try:
                val = float(line[var_len+3:line_len-2])
            except:
                val = line[var_len+3:line_len-2]
    
            setattr(grid_data, var, val)
        
        # Close the file.
        f.close()
        
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
            if hasattr(grid_data, 'min_'+dim):
                setattr(grid_data,dim+'lim',\
                        [getattr(grid_data,'min_'+dim),\
                         getattr(grid_data,'min_'+dim) + \
                         getattr(grid_data,'L'+dim)])
    
        return grid_data
    else:
        # Hard-coded back-up
        grid_data.nd = 3
    
        grid_data.Nx = 3072
        grid_data.Ny = 192
        grid_data.Nz = 192

    return grid_data
## ------