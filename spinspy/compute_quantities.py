import numpy as np
import spinspy as spy
import matplotlib.pyplot as plt
import warnings


class Compute():
    '''
    Class to hold information about quantities that are of interest in a simulation analysis
    '''

    def __init__(
        self,
        folder_path: str,
        time: int=None
    ):
        '''
        Initializes an object instance that stores folder information as well as
        the parameters of the simulation and optionally, reads the data associated with a given time

        Parameters
        ----------
        folder_path: str
            folder path to the folder containing simulation data for all times
        time: int, optional
            if this is given, the Compute object will only consider reading data and computing
            for a given time. This is an option that reduces overload by avoiding repeated reading
            calls.
        '''


        # Set folder path
        self.folder = folder_path
        spy.set_path(self.folder)
        # Read params of the simulation
        x, y, z, params = spy.get_gridparams()
        self.x = x
        self.y = y
        self.z = z
        self.params = params
        self.Nzf = 2 * self.params.Nz

        # Fourier quantities
        self.dk = 2 * np.pi / self.params.Lx
        self.dl = 2 * np.pi / self.params.Ly
        self.dm = 2 * np.pi / (2 * self.params.Lz) # TODO why?

        self.ksvec = np.concatenate([
            np.arange(0, self.params.Nx/2), 
            np.zeros(1), 
            np.arange(-self.params.Nx/2 + 1, 0)
        ]) * self.dk
        self.lsvec = np.concatenate([
            np.arange(0, self.params.Ny/2),
            np.zeros(1),
            np.arange(-self.params.Ny/2 + 1, 0)
        ]) * self.dl
        self.msvec = np.concatenate([
            np.arange(0, self.Nzf/2),
            np.zeros(1),
            np.arange(-self.Nzf/2 + 1, 0)
        ]) * self.dm

        self.knyq = np.max(np.abs(self.ksvec))
        self.lnyq = np.max(np.abs(self.lsvec))
        self.mnyq = np.max(np.abs(self.msvec))
        self.iks = np.zeros(shape=(self.params.Nx, 1, 1), dtype=np.complex128)
        self.ils = np.zeros(shape=(1, self.params.Ny, 1), dtype=np.complex128)
        self.ims = np.zeros(shape=(1, 1, self.Nzf), dtype=np.complex128)

        self.iks[:, 0, 0] = 1j * self.ksvec
        self.ils[0, :, 0] = 1j * self.lsvec
        self.ims[0, 0, :] = 1j * self.msvec

        self.ux = None
        self.uy = None
        self.uz = None
        self.vx = None
        self.vy = None
        self.vz = None
        self.wx = None
        self.wy = None
        self.wz = None

        if time is not None:
            self.time = time
            self._assign_velocity_derivatives(time)

    def ke(self, time: int=None):
        '''
        Calculates KE for time given or time stored in the Compute class

        Parameters
        ----------
        time: int

        Returns
        -------
        tuple: KE, KE3D and KE3D (with streamfunction)
        '''
        # change folder before every calculation
        spy.set_path(self.folder)

        if time is None:
            try:
                time = self.time # if self.time does not exist, an error will be thrown
                self._assign_velocity_derivatives(time)
            except Exception:
                print("'time' was not given, and it was not set when the class was instantiated.")

        u = spy.reader('u', time)
        v = spy.reader('v', time)
        w = spy.reader('w', time)
        u_mean_y = np.mean(u, axis=1) # average across y, numpy automatically squeezes out direction
        # tile the array along a third dimension (spanwise) so as to broadcast while removing the mean velocity
        u_mean_full = np.transpose(u_mean_y[:, :, np.newaxis], (0, 2, 1))
        ur = u - u_mean_full
        v_mean_y = np.mean(v, axis=1)
        v_mean_full = np.transpose(v_mean_y[:, :, np.newaxis], (0, 2, 1))
        vr = v - v_mean_full
        w_mean_y = np.mean(w, axis=1)
        w_mean_full = np.transpose(w_mean_y[:, :, np.newaxis], (0, 2, 1))
        wr = w - w_mean_full

        ke = 0.5 * (u**2 + v**2 + w**2)
        ke3d = 0.5 * (ur**2 + vr**2 + wr**2)
        ke3d2 = 0.5 * (ur**2 + v**2 + wr**2)

        return ke, ke3d, ke3d2


    def ke_all_times(
        self,
        init_time=0,
        fin_time=70,
        time_increment=5
    ):
        '''
        Function to compute the KE and 3D KE (Caulfield) given a folder with velocity
        data output from SPINS.

        Parameters
        ----------
        folder_path: str
        init_time: int
        fin_time: int
        time_increment: int

        Returns
        -------
        tuple: (ke, ke3d, ke3d_streamfunction)
        '''
        # change folder before every calculation
        spy.set_path(self.folder)

        # initialize ketot and ke3dtot arrays
        ketot = []
        ke3dtot = []
        ke3d2tot = []

        for i in np.arange(init_time, fin_time + 1, time_increment):
            u = spy.reader('u', i)
            v = spy.reader('v', i)
            w = spy.reader('w', i)
            u_mean_y = np.mean(u, axis=1) # average across y, numpy automatically squeezes out direction
            # tile the array along a third dimension (spanwise) so as to broadcast while removing the mean velocity
            u_mean_full = np.transpose(u_mean_y[:, :, np.newaxis], (0, 2, 1))
            ur = u - u_mean_full
            v_mean_y = np.mean(v, axis=1)
            v_mean_full = np.transpose(v_mean_y[:, :, np.newaxis], (0, 2, 1))
            vr = v - v_mean_full
            w_mean_y = np.mean(w, axis=1)
            w_mean_full = np.transpose(w_mean_y[:, :, np.newaxis], (0, 2, 1))
            wr = w - w_mean_full

            ke = 0.5 * (u**2 + v**2 + w**2)
            ke3d = 0.5 * (ur**2 + vr**2 + wr**2)
            ke3d2 = 0.5 * (ur**2 + v**2 + wr**2)
            ketot.append(np.sum(ke))
            ke3dtot.append(np.sum(ke3d))
            ke3d2tot.append(np.sum(ke3d2))
        
        ketotarray = np.array(ketot)
        ke3dtotarray = np.array(ke3dtot)
        ke3d2totarray = np.array(ke3d2tot)

        return ketotarray, ke3dtotarray, ke3d2totarray

    def enstrophy(self, time):
        '''
        Calculates the enstrophy at a given time.
        ''' 
        spy.set_path(self.folder)

        if time is None:
            try:
                time = self.time # if self.time does not exist, an error will be thrown
                self._assign_velocity_derivatives(time)
            except Exception:
                print("'time' was not given, and it was not set when the class was instantiated.")
        
        self._assign_velocity_derivatives()

        enst = 0.5 * (
            (self.wy - self.vz) ** 2 
            + (self.uz - self.wx) ** 2
            + (self.vx - self.uy) ** 2
            )
        return enst

    def vorticity(self, time):

        self._assign_velocity_derivatives(time)

        omega_x = self.wy - self.vz
        omega_y = self.uz - self.wx
        omega_z = self.vx - self.uy
        
        return omega_x, omega_y, omega_z

    def all_quantities(self, time):
        '''
        Computes the following quantities of interest for a given time:
            1. KE
            2. KE3d
            3. KE3d - preserving incompressibility / analytic
            4. Enstrophy
            5. Dissipation
            6. Vorticity (omega_x, omega_y, omega_z)
            7. Vortex stretching
            8. Q
            9. R
            10. Lambda 2
        '''

        spy.set_path(self.folder)

        final_dict = {}

        # reading data
        u = spy.reader('u', time)
        v = spy.reader('v', time)
        w = spy.reader('w', time)
        t = spy.reader('t', time)
        try:
            s = spy.reader('s', time)
        except:
            warnings.warn("No salinity information provided.", UserWarning)
        
        self._assign_velocity_derivatives(time)

        ke = 0.5 * (u ** 2 + v ** 2 + w ** 2) # KE
        
        u_mean_y = np.mean(u, axis=1)
        u_mean_full = np.transpose(u_mean_y[:, :, np.newaxis], (0, 2, 1))
        ur = u - u_mean_full
        v_mean_y = np.mean(v, axis=1)
        v_mean_full = np.transpose(v_mean_y[:, :, np.newaxis], (0, 2, 1))
        vr = v - v_mean_full
        w_mean_y = np.mean(w, axis=1)
        w_mean_full = np.transpose(w_mean_y[:, :, np.newaxis], (0, 2, 1))
        wr = w - w_mean_full

        ke3d = 0.5 * (ur ** 2 + vr ** 2 + wr ** 2)
        ke3d_incomp = 0.5 * (ur ** 2 + v ** 2 + wr ** 2)

        enstrophy = 0.5 * (
            (self.wy - self.vz) ** 2 
            + (self.uz - self.wx) ** 2
            + (self.vx - self.uy) ** 2
            )

        omega_x = self.wy - self.vz
        omega_y = self.uz - self.wx
        omega_z = self.vx - self.uy

        vortstretchx = omega_x * self.ux + omega_y * self.uy + omega_z * self.uz
        vortstretchy = omega_x * self.vx + omega_y * self.vy + omega_z * self.vz
        vortstretchz = omega_x * self.wx + omega_y * self.wy + omega_z * self.wz
        vortstretch = np.sqrt(vortstretchx ** 2 + vortstretchy ** 2 + vortstretchz ** 2)

        dissipation = 2 * self.params.visco * (
            self.ux ** 2 + self.vy ** 2 + self.wz ** 2 +
            0.5 * (self.uy + self.vx) ** 2 +
            0.5 * (self.uz + self.wx) ** 2 +
            0.5 * (self.vz + self.wy) ** 2
            )

        Q = (
            -0.5 * (self.ux ** 2 + self.vy ** 2 + self.wz ** 2) 
            - (self.uy * self.vx + self.uz * self.wx + self.vz * self.wy)
        )

        R = (
            self.ux * self.vy * self.wz
            + self.uy * self.vz * self.wx
            + self.uz * self.vx * self.wy
            - self.wx * self.vy * self.uz
            - self.wy * self.vz * self.ux
            - self.wz * self.vx * self.uy
        )

        # lambda 2
        mat = np.zeros(shape=(3, 3))
        lam2 = np.zeros(shape=(self.params.Nx, self.params.Ny, self.params.Nz))
        for i in range(self.params.Nx):
            for j in range(self.params.Ny):
                for k in range(self.params.Nz):
                    mat[0, 0] = self.ux[i, j, k]
                    mat[0, 1] = self.uy[i, j, k]
                    mat[0, 2] = self.uz[i, j, k]
                    mat[1, 0] = self.vx[i, j, k]
                    mat[1, 1] = self.vy[i, j, k]
                    mat[1, 2] = self.vz[i, j, k]
                    mat[2, 0] = self.wz[i, j, k]
                    mat[2, 1] = self.wy[i, j, k]
                    mat[2, 2] = self.wz[i, j, k]
                    s = 0.5 * (mat + mat.T)
                    om = 0.5 * (mat - mat.T)
                    matrix_for_lambda2 = np.matmul(s, s) + np.matmul(om, om)
                    lambda_eigs = np.sort(np.linalg.eig(matrix_for_lambda2)[0])
                    lam2[i, j, k] = lambda_eigs[1]
        
        final_dict['ke'] = ke
        final_dict['ke3d'] = ke3d
        final_dict['ke3d_incomp'] = ke3d_incomp
        final_dict['enstrophy'] = enstrophy
        final_dict['dissipation'] = dissipation
        final_dict['Q'] = Q
        final_dict['R'] = R
        final_dict['lambda2'] = lam2
        final_dict['vortstretch'] = vortstretch
        final_dict['vortx'] = omega_x
        final_dict['vorty'] = omega_y
        final_dict['vortz'] = omega_z

        return final_dict  


    def _assign_velocity_derivatives(self, time: int):
        '''
        Function used in another functions that require computation of velocity derivatives
        ux, uy, uz, vx ,vy, vz, wx, wy, wz and saves them as class variables

        Parameters
        ----------
        time: output number we want to compute these for

        Returns
        -------
        None
        '''
        spy.set_path(self.folder)
        # u
        u = spy.reader('u', time)
        temp = np.zeros(shape=(self.params.Nx, self.params.Ny, self.Nzf))
        temp[:, :, :self.params.Nz] = u
        temp[:, :, self.params.Nz:] = np.flip(u, 2)
        tempf = np.fft.fftn(temp) #fft
        tempfder = tempf * self.iks # x derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.ux = temp[:, :, :self.params.Nz]
        tempfder = tempf * self.ils # y derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.uy = temp[:, :, :self.params.Nz]
        tempfder = tempf * self.ims # z derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.uz = temp[:, :, :self.params.Nz]

        # v
        v = spy.reader('v', time)
        temp = np.zeros(shape=(self.params.Nx, self.params.Ny, self.Nzf))
        temp[:, :, :self.params.Nz] = v
        temp[:, :, self.params.Nz:] = np.flip(v, 2)
        tempf = np.fft.fftn(temp) #fft
        tempfder = tempf * self.iks # x derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.vx = temp[:, :, :self.params.Nz]
        tempfder = tempf * self.ils # y derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.vy = temp[:, :, :self.params.Nz]
        tempfder = tempf * self.ims # z derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.vz = temp[:, :, :self.params.Nz]

        # w
        w = spy.reader('w', time)
        temp = np.zeros(shape=(self.params.Nx, self.params.Ny, self.Nzf))
        temp[:, :, :self.params.Nz] = w
        temp[:, :, self.params.Nz:] = - np.flip(w, 2)
        tempf = np.fft.fftn(temp) #fft
        tempfder = tempf * self.iks # x derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.wx = temp[:, :, :self.params.Nz]
        tempfder = tempf * self.ils # y derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.wy = temp[:, :, :self.params.Nz]
        tempfder = tempf * self.ims # z derivative
        temp = np.real(np.fft.ifftn(tempfder)) # invert
        self.wz = temp[:, :, :self.params.Nz]

        return None