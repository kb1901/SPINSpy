import sys
import numpy as np
from spinspy import local_data

## -----------------
## Class for diagnostics
class Diagnostic:
    """ Class for handling diagnostics.
        
        At the moment, doesn't really do anything.
    """
## ----------------


## ------------------
## get_diagnostics: Parse diagnostics.txt
def get_diagnostics(fp = 'diagnostics.txt'):
    
    # Start by seeing how many lines there are
    num_lines = sum(1 for line in open(fp)) - 1

    fp = '{0:s}{1:s}'.format(local_data.prefix,fp)

    fid = open(fp, 'r')
    
    # Read the header files
    # We assume that they are comma separated.
    curr = fid.readline()
    fields = []
    ii,jj = 0,0
    while jj < len(curr):
        if (curr[jj] == ',') or jj == len(curr)-1:
            fields += [curr[ii:jj].strip()]
            jj += 1
            ii = jj
        jj += 1

    # Now, add the fields to the diagnostics object
    diagnostics = Diagnostic()
    diagnostics.nVar = len(fields)
    values = []
    for ii in range(len(fields)):
        values += [np.zeros(num_lines)]

    # Now loop through the rest of the lines.
    # Again, assume that values are comma separated.
    
    curr = fid.readline()
    line_num = 0
    while curr != '':
        ii,jj = 0,0
        var_num = 0
        while jj < len(curr):
            if (curr[jj] == ',') or jj == len(curr)-1:
                val = float(curr[ii:jj].strip())
                values[var_num][line_num] = val 
                jj += 1
                ii = jj
                var_num += 1
            jj += 1
        line_num += 1
        curr = fid.readline()
 
    fid.close()

    for ii in range(len(fields)):
        setattr(diagnostics,fields[ii],values[ii])

    return diagnostics
# ------------------
