import matpy as mp
import numpy as np
import spinspy as spy
import matplotlib.pyplot as plt

# take Ly/2 as an argument for slice. Is it possible?

def plot2d(var, t_index,
           dimen='Y', slice=0, axis='Full',
           xskp=1, yskp=1, zskp=1,
           style='contourf', ncontourf=40, ncontour=10,
           contour2='rho', ncontour2=6,
           colorbar=True,
           fnum=1, savefig=False, visible=True
           ):

    # Initialize figure
    fig = plt.figure(fnum)
    if len(t_index)>1:
        plt.ion()

    # Get grid
    gd = spy.get_grid()  # fix to only read in once, not every function call
    params = spy.get_params()

    # get indices of plotting area
    if axis != 'Full' and (len(axis) != 4 or (axis[0]>axis[1] or axis[2]>axis[3])):
        msg = 'Axis must be of correct size and order [x_left, x_right, y_bottom, y_top].'
        raise SillyHumanError(msg)
    else:
        nx, ny, nz, xvar, yvar = findindices(gd, params, dimen, slice, axis, xskp, yskp, zskp)

    for ii in t_index:
        # read data 
        data = spy.reader(var, ii, nx, ny, nz)

        # make plot
        if style == 'pcolor':
            plt.pcolormesh(xvar, yvar, data.T, cmap=mp.darkjet)
            cont2col = 'w'
        elif style == 'contourf':
            plt.contourf(xvar, yvar, data.T, ncontourf, cmap=mp.darkjet)
            cont2col = 'w'
        elif style == 'contour':
            plt.contour(xvar, yvar, data.T, ncontour, cmap=mp.darkjet)
            cont2col = 'k'

        # colorbar work and limits
    

        # Add contours of secondary field (typically density)
        if contour2 != 'None':
            if contour2 != var:
                data2 = spy.reader(contour2, ii, nx, ny, nz)
                plt.contour(xvar, yvar, data2.T, ncontour2, colors=cont2col)

        plt.title(var+', '+dimen+'={:g} m, t_n={:d}'.format(*(slice, ii)))
        if dimen == 'X':
            plt.xlabel(r"$y$ (m)")
            plt.ylabel(r"$z$ (m)")
        if dimen == 'Y':
            plt.xlabel(r"$x$ (m)")
            plt.ylabel(r"$z$ (m)")
        if dimen == 'Z':
            plt.xlabel(r"$x$ (m)")
            plt.ylabel(r"$y$ (m)")
        plt.draw()

    plt.show()


def findindices(gd, params, dimen, slice, axis, xskp, yskp, zskp):

    x1d = gd[0]
    y1d = gd[1]
    z1d = gd[2]
    Nx = params.Nx
    Ny = params.Ny
    Nz = params.Nz
    if dimen == 'X':
        # if cross-section is in y-z plane
        nx = spy.nearestindex(x1d, slice)
        if axis == 'Full':
            ny = range(0, Ny, yskp)
            nz = range(0, Nz, zskp)
        else:  # find indices for a smaller plotting area
            lft = spy.nearestindex(y1d, axis[0])
            rht = spy.nearestindex(y1d, axis[1])
            bot = spy.nearestindex(z1d, axis[2])
            top = spy.nearestindex(z1d, axis[3])
            ny = range(lft, rht, yskp)
            nz = range(bot, top, zskp)
        # set axis to use in plot
        xvar = y1d[ny]
        yvar = z1d[nz]
        #plotaxis = [y1d(ny[0])]
    elif dimen == 'Y':
        # if cross-section is in x-z plane
        ny = spy.nearestindex(y1d, slice)
        if axis == 'Full':
            nx = range(0, Nx, xskp)
            nz = range(0, Nz, zskp)
        else:  # find indices for a smaller plotting area
            lft = spy.nearestindex(x1d, axis[0])
            rht = spy.nearestindex(x1d, axis[1])
            bot = spy.nearestindex(z1d, axis[2])
            top = spy.nearestindex(z1d, axis[3])
            nx = range(lft, rht, xskp)
            nz = range(bot, top, zskp)
        # set axis to use in plot
        xvar = x1d[nx]
        yvar = z1d[nz]
    elif dimen == 'Z':
        # if cross-section is in x-y plane
        nz = spy.nearestindex(z1d, slice)
        if axis == 'Full':
            nx = range(0, Nx, xskp)
            ny = range(0, Ny, yskp)
        else:  # find indices for a smaller plotting area
            lft = spy.nearestindex(x1d, axis[0])
            rht = spy.nearestindex(x1d, axis[1])
            bot = spy.nearestindex(y1d, axis[2])
            top = spy.nearestindex(y1d, axis[3])
            nx = range(lft, rht, xskp)
            ny = range(bot, top, yskp)
        # set axis to use in plot
        xvar = x1d[nx]
        yvar = y1d[ny]

    return nx, ny, nz, xvar, yvar
