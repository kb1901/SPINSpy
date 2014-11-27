import numpy as np
import sys
import collections
import os
import warnings

## Create some error classes
## ------
class Error(Exception):
    """ Base class for exceptions in this module. """
    pass

class SillyHumanError(Error):
    """ Exception raised when the human does something silly.
        
        Attributes:
            msg -- explanation of the error"""

    def __init__(self, msg):
        self.msg = msg
        print(msg)
##------

## Create grid class
## ------
class Grid():
    
    def __init__(self):
        # Number of dimensions
        self.nd = None

        # Number of gridpoints
        self.Nx = None
        self.Ny = None
        self.Nz = None
    
        # Domain lengths
        self.Lx = None
        self.Ly = None
        self.Lz = None
    
        # Domain limits [min, max]
        self.xlim = None
        self.ylim = None
        self.zlim = None
    
        # Grid types
        self.xtype = None
        self.ytype = None
        self.ztype = None
    
    def display(self):
        
        print('{0}-dimensional simulation:'.format(self.nd))

        if self.nd >= 1:
            print('First Dimension: (x)')
        
            if self.Nx == None:
                print('  Number of Points: n/a')
            else:
                print('  Number of Points: {0:d}'.format(self.Nx))
        
            if self.Lx == None:
                print('  Length of Domain: n/a')
            else:
                print('  Length of Domain: {0:1.4e}'.format(self.Lx))

            if self.xlim == None:
                print('  Bounds of Domain: n/a')
            else:
                print('  Boundas of Domain: {0}, {1}'.format(self.xlim[0], self.xlim[1]))

        if self.nd >= 2:
            print('Second Dimension: (y)')

            if self.Ny == None:
                print('  Number of Points: n/a')
            else:
                print('  Number of Points: {0:d}'.format(self.Ny))

            if self.Ly == None:
                print('  Length of Domain: n/a')
            else:
                print('  Length of Domain: {0:1.4e}'.format(self.Ly))

            if self.ylim == None:
               print('  Bounds of Domain: n/a')
            else:
                print('  Boundas of Domain: {0:1.4e}, {1:1.4e}'\
                      .format(self.ylim[0], self.ylim[1]))

        if self.nd >=3:
            print('Third Dimension: (z)')

            if self.Nz == None:
                print('  Number of Points: n/a')
            else:
                print('  Number of Points: {0:d}'.format(self.Nz))

            if self.Lz == None:
                print('  Length of Domain: n/a')
            else:
                print('  Length of Domain: {0:1.4e}'.format(self.Lz))

            if self.zlim == None:
                print('  Bounds of Domain: n/a')
            else:
                print('  Boundas of Domain: {0:1.4e}, {1:1.4e}'\
                      .format(self.zlim[0], self.zlim[1]))

## ------

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


## Create reader files for SPINS outputs
## ------
def reader(var, *args, **kwargs):
    # This is a python version of the *_reader.m files
    # produced my SPINS for the purpose of parsing SPINS
    # outputs. The input arguments and usage are as follows:
    
    # var:
    #       type = str
    #       purpose: the variable to be loaded
    #       examples: 'rho', 'u', 'x'
    
    # seq:
    #       type = int (or integer-valued float)
    #       purpose: the time-step index
    #       examples: var = 'u', seq = 15 loads u.15
    
    # xs,ys,zs:
    #       type = int or list of ints
    #       purpose: slices the data at the appropriate indices
    #           if int (or 1-element list)
    #               - slices a single index
    #           if 2-element list [a,b]
    #               - shorthand for a:b-1
    #               - [0,-1] gets everything
    #           else
    #               - selects at the given indices
    
    # type (optional):
    #       type = str
    #       default = 'ndarray'
    #       purpose: Allows the user to choose if the output should
    #                be a numpy ndarray or the memory map object.
    #       options:
    #           'ndarray' (default): produces a numpy ndarray
    #           'memmap': returns the memory map
    
    # ordering (optional):
    #       type = str
    #       default = 'natural'
    #       purpose: Allows the user to choose natural (x,y,z) ordering,
    #                or MATLAB ordering (y,x,z).
    #       options:
    #           'natural' (default): [x,y,z] ordering
    #           'matlab': [y,x,z] ordering
    
    grid_data = get_shape()
    
    # Parse args
    nargs = len(args)
    if (var == 'x') | (var == 'y') | (var == 'z'):
        # Grids don't have seq arguments, only xs, ys, and zs.
        xs = args[0]
        ys = args[1]
        if nargs == 3:
            # 3 -> 3D
            zs = args[2]
        elif nargs == 2:
            # 2 -> 2D
            pass
    else:
        seq = args[0]
        xs = args[1]
        ys = args[2]
        if nargs == 4:
            # 4 -> 3D (less one for seq)
            zs = args[3]
        elif nargs == 3:
            # 3 -> 2D (less one for seq)
            pass

    # Parse kwargs
    # We just need to check which keywords arguments
    # have been set and then set any missing ones.
    if 'ordering' in kwargs:
        ordering = kwargs['ordering']
    else:
        ordering = 'natural'

    if 'type' in kwargs:
        out_type = kwargs['type']
    else:
        out_type = 'ndarray'

    # Parse the indexes
    if grid_data.nd == 3:
        xs = Parse_Index(xs,0,grid_data.Nx)
        ys = Parse_Index(ys,0,grid_data.Ny)
        zs = Parse_Index(zs,0,grid_data.Nz)
    elif grid_data.nd == 2:
        xs = Parse_Index(xs,0,grid_data.Nx)
        ys = Parse_Index(ys,0,grid_data.Ny)

    # File to load
    if (var == 'x') | (var == 'y') | (var == 'z'):
        fname = '{0:s}grid'.format(var)
    else:
        fname = '{0:s}.{1:d}'.format(var,seq)

    # Does the requested file exist?
    if not(os.path.isfile(fname)):
        err_msg = 'The requested file, {0:s}, does not exist.'.format(fname)
        raise SillyHumanError(err_msg)

    # Determine endianness
    endian = sys.byteorder
    if endian == 'little':
        dt = np.dtype('<d')
    else:
        dt = np.dtype('>d')

    # Create the memory map
    if grid_data.nd == 3:
        m = np.memmap(fname, dtype=dt, mode='r',
                      shape=(grid_data.Nx,grid_data.Nz,grid_data.Ny))
        m = np.swapaxes(m, 1, 2) # Order to [x,y,z]
        m = m[xs,:,:][:,ys,:][:,:,zs]
        m = np.squeeze(m)
        if ordering == 'matlab':
            m = np.swapaxes(m, 0, 1) # Order to [y,x,z] if desired.
        elif ordering != 'natural':
            # There are no other options, silly human.
            raise SillyHumanError('Ordering choice ({0:s}) not recognized.'.format(ordering))
    elif grid_data.nd == 2:
        m = np.memmap(fname, dtype=dt, mode='r',
                      shape=(grid_data.Nx,grid_data.Ny))
        m = m[xs,:][:,ys]
        m = np.squeeze(m)
        if ordering == 'matlab':
            m = np.swapaxes(m, 0, 1) # Order to [y,x] if desired.
        elif ordering != 'natural':
            # There are no other options, silly human.
            raise SillyHumanError('Ordering choice ({0:s}) not recognized.'.format(ordering))


    if out_type == 'ndarray':
        m=m.view(type=np.ndarray)
    elif out_type == 'memmap':
        # Nothing to do
        pass
    else:
        # Raise an error .
        raise SillyHumanError('Requestion output type "{0:s}" is unknown.'.format(out_type))

    return m

def Parse_Index(ind, lb, ub):
    
    if isinstance(ind, collections.Sequence):
    # If the input was a list (or tuple), then work with that
        if len(ind) == 1:
            # If it's a one-element list, treat that as a single slice request
            ind = [ind[0]]
        elif len(ind) == 2:
            # A 2-element list is short-hand. [a,b] -> a:b-1
            # Negative values are permitted, and refer to distance from end.
            if (ind[0] < lb):
                ind[0] = (ind[0] % ub) + 1
            if (ind[1] >= ub):
                warnings.warn('Requested index exceeds size. Truncating request.')
                ind[1] = ub
            elif (ind[1] < 0):
                ind[1] = (ind[1] % ub) + 1
            ind = range(ind[0],ind[1])
    else:
        ind = [ind]


    return ind
## ------