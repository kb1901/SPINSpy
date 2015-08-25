import matplotlib
matplotlib.use('Agg')
import matpy as mp
import numpy as np
import spinspy as spy
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sys, os, shutil, tempfile
import subprocess
from mpl_toolkits.axes_grid1 import make_axes_locatable

try: # Try using mpi
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    num_procs = comm.Get_size()
except:
    rank = 0
    num_procs = 1

## USER CHANGE THIS SECTION
out_direct = os.getcwd() # Where to put the movies
                                    #   the directory needs to already exist!
the_name = '2D_Turbulence'          # What to call the movies
                                    #   the variable name will be appended
out_suffix = 'mp4'                  # Movie type
mov_fps = 15                        # Framerate for movie
cmap = 'darkjet'

# Load some information
dat = spy.get_shape()
x,y = spy.grid()

##

## USER SHOULDN'T NEED TO CHANGE ANYTHING AFTER THIS
# Prepare directories
if rank == 0:
    print('Video files will be saved in {0:s}'.format(out_direct))
    tmp_dir = tempfile.mkdtemp(dir=out_direct)
    fig_prefix = tmp_dir + '/' + the_name # path for saving frames
    out_prefix = out_direct + '/' + the_name # path for saving videos
    for proc in range(1,num_procs):
        comm.send(tmp_dir,dest=proc,tag=1)
        comm.send(fig_prefix,dest=proc,tag=2)
        comm.send(out_prefix,dest=proc,tag=3)
else:
    tmp_dir = comm.recv(source=0,tag=1)
    fig_prefix = comm.recv(source=0,tag=2)
    out_prefix = comm.recv(source=0,tag=3)

# Initialize the three meshes
fig = plt.figure()
plt.title('q')
sp1 = plt.subplot(1,1,1)

# Initial pcolormesh objects
QM1 = plt.pcolormesh(x/1e3,y/1e3,np.zeros((dat.Ny,dat.Nx)),cmap=cmap)
plt.axis('tight')

# Initialize colorbars
div1 = make_axes_locatable(sp1)
cax1 = div1.append_axes("bottom", size="5%", pad=0.25)
cbar1 = plt.colorbar(QM1, cax=cax1, format="%.2g", orientation='horizontal')
cax1.yaxis.set_visible(False)
cax1.set_xticklabels(cax1.get_xticklabels(),rotation=70,ha='center')

# Start at var0 and keep going until we run out.
ii = rank # parallel, so start where necessary
cont = True

while cont:
    try:
        q_ii = spy.reader('q',ii,[0,-1],[0,-1],ordering='matlab')

        if ii % 1 == 0:
            print('Processor {0:d} accessing {1:d}'.format(rank,ii))

        # Now trim off the last row and column of to_plt.
        # Why? Because it's going to anyways (unless X1 and X2)
        # are 1 bigger in each direction, which, if it's SPINS,
        # it won't. Normally this wouldn't be a problem, but
        # in this case it is because we are updating a plot, a
        # process that requires ravel, so it gets confused about
        # what it needs to trim, so we pre-trim for it.
        q_ii = q_ii[:-1,:-1]

        QM1.set_array(np.ravel(q_ii))

        cv_xy = np.max(np.abs(np.ravel(q_ii)))

        if cv_xy == 0:
            cv_xy = 1
            
        QM1.set_clim((-cv_xy,cv_xy))
        QM1.changed()

        fig.suptitle('ii = {0:04d}'.format(ii))
        plt.draw()
        fig.savefig('{0:s}-{1:05d}.png'.format(fig_prefix,ii))
        ii += num_procs # Parallel, so skip a `bunch'
    except:
        cont = False
        var_figs = '{0:s}-%05d.png'.format(fig_prefix)

# Have processor 0 wait for the others
if num_procs > 1:
    if rank > 0:
        isdone = True
        comm.send(isdone, dest=0, tag=rank)
        print('Processor {0:d} done.'.format(rank))
    elif rank == 0:
        isdone = False
        for proc in range(1,num_procs):
            isdone = comm.recv(source=proc,tag=proc)

# Now that the individual files have been written, we need to parse them into a movie.
if rank == 0:
    in_name  = var_figs
    out_name = '{0:s}.{1:s}'.format(out_prefix,out_suffix)
    cmd = ['ffmpeg', '-framerate', str(mov_fps), '-r', str(mov_fps),
        '-i', in_name, '-y', '-q', '1', '-pix_fmt', 'yuv420p', out_name]
    subprocess.call(cmd)

    print('--------')
    print('Deleting directory of intermediate frames.')
    shutil.rmtree(tmp_dir)
    print('Video creation complete.')
    print('Processor {0:d} done.'.format(rank))
