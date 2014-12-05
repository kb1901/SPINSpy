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
                print('  Length of Domain: {0:1.3e}'.format(self.Lx))

            if self.xlim == None:
                print('  Bounds of Domain: n/a')
            else:
                print('  Boundas of Domain: {0:1.3e}, {1:1.3e}'.format(self.xlim[0], self.xlim[1]))
                    
            if hasattr(self, 'type_x'):
                print('  Type: {0:s}'.format(self.type_x))

        if self.nd >= 2:
            print('Second Dimension: (y)')

            if self.Ny == None:
                print('  Number of Points: n/a')
            else:
                print('  Number of Points: {0:d}'.format(self.Ny))

            if self.Ly == None:
                print('  Length of Domain: n/a')
            else:
                print('  Length of Domain: {0:1.3e}'.format(self.Ly))

            if self.ylim == None:
               print('  Bounds of Domain: n/a')
            else:
                print('  Boundas of Domain: {0:1.3e}, {1:1.3e}'\
                      .format(self.ylim[0], self.ylim[1]))
            
            if hasattr(self, 'type_y'):
                print('  Type: {0:s}'.format(self.type_y))

        if self.nd >=3:
            print('Third Dimension: (z)')

            if self.Nz == None:
                print('  Number of Points: n/a')
            else:
                print('  Number of Points: {0:d}'.format(self.Nz))

            if self.Lz == None:
                print('  Length of Domain: n/a')
            else:
                print('  Length of Domain: {0:1.3e}'.format(self.Lz))

            if self.zlim == None:
                print('  Bounds of Domain: n/a')
            else:
                print('  Boundas of Domain: {0:1.3e}, {1:1.3e}'\
                      .format(self.zlim[0], self.zlim[1]))
            
            if hasattr(self, 'type_z'):
                print('  Type: {0:s}'.format(self.type_z))

## ------