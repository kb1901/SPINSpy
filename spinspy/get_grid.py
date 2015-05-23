from reader import reader
from get_params import get_params
from isdim import isdim

## Read in the grid as either vectors (1)
## or full matrices (2).
## (1) x,y[,z] = spinspy.grid()
## (2) x,y[,z] = spinspy.grid(type='full')
## ------
def get_grid(type='vector'):
    
    grid_data = get_params()

    if grid_data.nd == 2:
        sel1 = ([0,-1],0)
        sel2 = (0,[0,-1])
        sel3 = ([0,-1], [0,-1])
        if type == 'vector':
            if isdim('x'):
                X1 = reader('x', *sel1)
                if isdim('y'):
                    X2 = reader('y', *sel2)
                elif isdim('z'):
                    X2 = reader('z', *sel2)
            else:
                X1 = reader('y', *sel1)
                X2 = reader('z', *sel2)
        elif type == 'full':
            if isdim('x'):
                X1 = reader('x',*sel3)
                if isdim('y'):
                    X2 = reader('y', *sel3)
                elif isdim('z'):
                    X2 = reader('z', *sel3)
            else:
                X1 = reader('y', *sel3)
                X2 = reader('z', *sel3)
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
        return X1,X2
    elif grid_data.nd == 3:
        return x,y,z
## ------
