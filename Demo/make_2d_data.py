import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftn, ifftn
import sys
import matpy

#######################################################
#         Flux for QG                                 #
#######################################################

def flux_qg_spec(q, parms): 

    q_hat = fftn(q)

    # Compute physical velocities
    u = (ifftn(-parms.ikyoK2*q_hat)).real
    v = (ifftn( parms.ikxoK2*q_hat)).real

    # Compute gradient of PV
    q_x = (ifftn( parms.ikx*q_hat)).real
    q_y = (ifftn( parms.iky*q_hat)).real

    # Compute flux
    flux = - u*q_x - v*(q_y + parms.beta)

    return flux
#######################################################
#        Parameters Class                             #
#######################################################

class Parms(object):
    """A class to solve the one-layer QG model."""
    
    def __init__(self):

        sc = 1
        nx = 128*sc
        ny = 128*sc
        Lx = 100e3
        Ly = 100e3
        beta = 0.e-11*1e4
        dt = 3600./80./sc
        tplot = 60.*dt*sc
        tmax = 3600.*24.
        Urms = 4.0
        rd  = 1.e7
        
        # put all the parameters into the object
        # grid
        self.nx = nx
        self.ny = ny
        self.Lx = Lx
        self.Ly = Ly

        # physical
        self.beta = beta
        
        # timestepping
        self.dt = dt
        self.tplot = tplot
        self.nt = int(tmax/dt)
        
        # define grid
        dx = Lx/nx
        dy = Ly/ny
        self.dx = dx
        self.dy = dy
        x = np.linspace(-Lx/2+dx/2,Lx/2-dx/2,nx)
        y = np.linspace(-Ly/2+dy/2,Ly/2-dy/2,ny)

        X,Y = np.meshgrid(x,y)
        X.T.tofile('Data/2d/xgrid')
        Y.T.tofile('Data/2d/ygrid')
        
        # pick method
        method = flux_qg_spec
        self.method = method
        
        if method == flux_qg_spec:
            # define wavenumbers
            kx = 2*np.pi/Lx*np.hstack([range(0,nx/2+1), range(-nx/2+1,0)])
            ky = 2*np.pi/Ly*np.hstack([range(0,ny/2+1), range(-ny/2+1,0)])
            kxx, kyy = np.meshgrid(kx,ky)
            K2 = (kxx**2 + kyy**2)
            self.ikx = 1j*kxx
            self.iky = 1j*kyy
            self.ikxoK2 = -1j*kxx/(K2 + 1/rd**2)
            self.ikyoK2 = -1j*kyy/(K2 + 1/rd**2)
        
            # define filter
            kmax = np.max(kx)
            ks = 0.4*kmax;
            km = 0.5*kmax;
            alpha = 0.69*ks**(-1.88/np.log(km/ks));
            beta  = 1.88/np.log(km/ks);
            self.sfilt = np.exp(-alpha*(kxx**2 + kyy**2)**(beta/2.0))

        # Write variables to file
        text_file = open("Data/2d/spins.conf", "w")

        text_file.write("Nx  = {0:d} \n".format(nx))
        text_file.write("Ny  = {0:d} \n".format(ny))
        text_file.write("Nz  = 1 \n")

        text_file.write("Lx  = {0:.12g} \n".format(Lx))
        text_file.write("Ly  = {0:.12g} \n".format(Ly))

        text_file.write("dt = {0:.12g} \n".format(dt))
        text_file.write("beta= {0:.12g} \n".format(beta))
        text_file.write("rd= {0:.12g} \n".format(rd))
        text_file.write("tmax= {0:.12g} \n".format(tmax))
        text_file.write("tplot= {0:.12g} \n".format(tplot))

        text_file.close()

#######################################################
#        Solve PDE                                    #
#######################################################

def solve_qg(parms, q0):   
    
    # Euler Step
    t = 0.
    ii = 0
    NLnm = parms.method(q0, parms)
    q    = q0 + parms.dt*NLnm;

    # AB2 step
    t = parms.dt
    ii = 1
    NLn = parms.method(q, parms)
    q   = q + 0.5*parms.dt*(3*NLn - NLnm)

    npt = int(parms.tplot/parms.dt)
    for ii in range(3,parms.nt+1):

        # AB3 step
        t = (ii-1)*parms.dt
        NL = parms.method(q, parms);
        q  = q + parms.dt/12*(23*NL - 16*NLn + 5*NLnm)
        q  = (ifftn(parms.sfilt*fftn(q))).real

        # Reset fluxes
        NLnm = NLn
        NLn  = NL

        if ii%npt==0:

            q.T.tofile('Data/2d/q.{0:d}'.format(ii/npt))

#######################################################
#         Main Program                                #
#######################################################

# Set parameters and specify initial conditions
parms = Parms() 
q0hat = np.random.randn(parms.ny,parms.nx) + 1j*np.random.randn(parms.ny,parms.nx)
q0 = ifftn(q0hat).real
q0.T.tofile('Data/2d/q.0')

# Solve
print('Creating 2D data...')
solve_qg(parms, q0)
print('Done!')


