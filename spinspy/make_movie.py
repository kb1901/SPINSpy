import matplotlib
matplotlib.use('Agg')
import matpy as mp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

def make_movie_2d(var, indx=[0,-1], mov_fps=15,
                       indy=[0,-1], mov_dpi=800):

    # Initialize figure
    fig = plt.figure()

    # Initialize the movie data
    FFMPEG = anim.writers['ffmpeg']
    writer = FFMPEG(fps=mov_fps)
    writer.setup(fig, out_name, mov_dpi)

    # Get the simulation data
    dat = spy.get_shape()
    x,y = spy.grid()

    cont = True
    ii = 1
    
    # Initialize the plot
    QMesh = plt.pcolormesh(x,y,np.zeros(dat.Ny,dat.Nx), cmap='darkjet')
    cbr = plt.colorbar(format='%.2e')
    # Start at var0 and keep going until we run out.
    while cont:
        try:
            to_plot = spy.reader(var,ii,indx,indy)
            cv = np.max(np.abs(np.ravel(to_plot)))
            QMesh.set_array(np.ravel(to_plot))
            if cv == 0:
                cv = 1
            QMesh.set_clim((-cv,cv))
            QMesh.changed()
            plt.draw()
            writer.grab_frame()
            ii += 1
        except:
            cont = False

    writer.finish()
    print('{0:d} frames processed. Figure saved in {1:s}'.format(ii,out_name))

def make_movie_3d(var, indx=[0,-1], mov_fps=15,
                       indy=[0,-1], mov_dpi=800,
                       indz=[0]):               
    # Initialize figure
    fig = plt.figure()

    # Initialize the movie data
    FFMPEG = anim.writers['ffmpeg']
    writer = FFMPEG(fps=mov_fps)
    writer.setup(fig, out_name, mov_dpi)

    # Get the simulation data
    dat = spy.get_shape()
    x,y,z = spy.grid()

    # Determine which way we're slicing
    if len(indz) == 1:
        X1 = x
        X2 = y
        N1 = dat.Ny
        N2 = dat.Nx
    elif len(indy) == 1:
        X1 = x
        X2 = z
        N1 = dat.Nz
        N2 = dat.Nx
    elif len(indx) == 1:
        X1 = y
        X2 = z
        N1 = dat.Nz
        N2 = dat.Ny
    else:
        pass

    cont = True
    ii = 1
    
    # Initialize the plot
    QMesh = plt.pcolormesh(x,y,np.zeros(N1,N2), cmap='darkjet')
    cbr = plt.colorbar(format='%.2e')
    
    # Start at var0 and keep going until we run out.
    while cont:
        try:
            to_plot = spy.reader(var,ii,indx,indy,indz)
            cv = np.max(np.abs(np.ravel(to_plot)))
            QMesh.set_array(np.ravel(to_plot.transpose()))
            if cv == 0:
                cv = 1
            QMesh.set_clim((-cv,cv))
            QMesh.changed()
            plt.draw()
            writer.grab_frame()
            ii += 1
        except:
            cont = False

    writer.finish()
    print('{0:d} frames processed. Figure saved in {1:s}'.format(ii,out_name))
