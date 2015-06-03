import os

def isdim(dim):
    if os.path.isfile('{0:s}grid'.format(dim)):
        return True
    else:
        return False
