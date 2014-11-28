from reader import reader
from get_shape import get_shape
from spinspy_classes import Grid

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