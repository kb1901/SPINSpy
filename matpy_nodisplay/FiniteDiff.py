import numpy as np
import numpy.linalg as nlg
import scipy
import scipy.sparse as sp
from scipy.misc import factorial
import scipy.linalg as spalg

## FiniteDiff computes FD matrices
## ------
def FiniteDiff(x, n, spb=True, uniform=True):

    #FiniteDiff : Create a finite difference matrix of arbitrary order for an
    #arbitrary grid.
    n = int(n)
    if len(x) == 3:
        # Using a length of 3 is shorthand. x = [a,b,c] is interpreted as
        # x = linspace(a,b,c). The advantage is that we don't actually need
        # to generate x, so we can save on memory when we want large grids.
        Nx = x[2]
    else:
        Nx = len(x)
    
    if spb:
        Dx = sp.lil_matrix((Nx, Nx))
    else:
        Dx = np.zeros([Nx, Nx])
    
    if uniform:
        if len(x) == 3:
            # Using a length of 3 is shorthand. x = [a,b,c] is interpreted as
            # x = linspace(a,b,c). The advantage is that we don't actually need
            # to generate x, so we can save on memory when we want large grids.
            dx = (x[1] - x[0])/float((x[2]-1))
        else:
            dx = x[1] - x[0];
        
        # Deal with boundary issues
        for i in range(0,int(np.ceil(n/2.0))):
            A = np.zeros([n+1,n+1])
            for j in range(0,n+1):
                A[:,j] = np.power(((j-i)*dx)*np.ones([1,n+1]),range(0,n+1))/factorial(range(0,n+1))
            b = np.zeros(n+1)
            b[1] = 1
            coeff = nlg.solve(A,b)
            coeff = coeff.conj().transpose()
            Dx[i, 0:n+1] = coeff
        
        for i in range(Nx-int(np.ceil(n/2)),Nx):
            A = np.zeros([n+1,n+1])
            for j in range(Nx-n-1,Nx):
                A[:,j-Nx+n+1] = np.power(((j-i)*dx)*np.ones([1,n+1]),range(0,n+1))/factorial(range(0,n+1))
            b = np.zeros(n+1)
            b[1] = 1
            coeff = nlg.solve(A,b)
            coeff = coeff.conj().transpose()
            Dx[i, Nx-n-1:Nx] = coeff
        
        # Now do the internals.
        A = np.zeros([n+1,n+1])
        if n % 2 == 0: # If even...
            for j in range(-n/2-1,n/2):
                A[:,j+n/2+1] = np.power(((j+1)*dx)*np.ones([1,n+1]),range(0,n+1))/factorial(range(0,n+1))
            b = np.zeros(n+1)
            b[1] = 1
            #print A
            #print b
            coeff = nlg.solve(A,b)
            coeff = coeff.conj().transpose()
            coeff = np.tile(coeff, [Nx, 1])
            Dx[n/2:Nx-n/2,:] = sp.spdiags(coeff.T, range(0,n+1), Nx-n, Nx).todense()
        elif n % 2 == 1: # If odd...
            for j in range(int(-np.floor(n/2.0))-1,int(np.ceil(n/2.0))):
                A[:,j+int(np.floor(n/2.0))+1] = \
                np.power(j*dx*np.ones([1,n+1]),range(0,n+1))\
                    /factorial(range(0,n+1))
            b = np.zeros(n+1)
            b[1] = 1;
            coeff = nlg.solve(A,b)
            coeff = coeff.conj().transpose()
            coeff = np.tile(coeff, [Nx, 1])
            Dx[int(np.ceil(n/2.0)):Nx-int(np.floor(n/2.0)),:] = sp.spdiags(coeff.T, range(0,n+1), Nx-n, Nx).todense()
    else:
        for i in range(0,Nx):
            if i < np.ceil(n/2.0):
                # Deal with 'left' boundary issues
                # Strict inequality since we index from 0
                A = np.zeros([n+1,n+1])
                for j in range(0,n+1):
                    dx = x[j]-x[i]
                    A[:,j] = (dx**range(0,n+1))/factorial(range(0,n+1))
                b = np.zeros(n+1)
                b[1] = 1
                coeff = nlg.solve(A,b)
                coeff = coeff.conj().transpose()
                Dx[i, 0:n+1] = coeff
            elif i >= Nx - np.ceil(n/2.0):
                # Deal with 'right' boundary issues
                # Non-strict because of 0 indexing
                A = np.zeros([n+1,n+1])
                for j in range(Nx-n-1,Nx):
                    dx = x[j]-x[i]
                    A[:,j-Nx+n+1] = (dx**range(0,n+1))/factorial(range(0,n+1));
                b = np.zeros(n+1)
                b[1] = 1
                coeff = nlg.solve(A,b)
                coeff = coeff.conj().transpose()
                Dx[i, Nx-n-1:Nx] = coeff
            else:
                # Deal with the internal pieces
                # If n is even, then just use a centred scheme
                if n % 2 == 0:
                    A = np.zeros([n+1,n+1])
                    for j in range(-n/2,n/2+1):
                        dx = x[i+j] - x[i]
                        A[:,j+n/2] = (dx**range(0,n+1))/factorial(range(0,n+1))
                    b = np.zeros(n+1)
                    b[1] = 1;
                    coeff = nlg.solve(A,b)
                    coeff = coeff.conj().transpose()
                    Dx[i, i-n/2:i+n/2+1] = coeff
            
                # If n is odd, then bias to which side has the closest point.
                elif n % 2 == 1:
                    
                    FLn = int(np.floor(n/2.0))
                    CLn = int(np.ceil(n/2.0))
                    
                    if abs(x[i+CLn] - x[i]) <= abs(x[i-CLn] - x[i]):
                        # If the right end is closer
                        A = np.zeros([n+1,n+1])
                        for j in range(-FLn,CLn+1):
                            dx = x[i+j] - x[i]
                            A[:,j+FLn] = (dx**range(0,n+1))/factorial(range(0,n+1))
                        b = np.zeros(n+1)
                        b[1] = 1
                        coeff = nlg.solve(A,b)
                        coeff = coeff.conj().transpose()
                        Dx[i, i-FLn:i+CLn+1] = coeff
                    
                    else:
                        # If the left end is closer
                        A = np.zeros([n+1,n+1])
                        for j in range(-CLn,CLn):
                            dx = x[i+j] - x[i]
                            A[:,j+CLn] = (dx**range(0,n+1))/factorial(range(0,n+1))
                        b = np.zeros(n+1)
                        b[1] = 1
                        coeff = nlg.solve(A,b)
                        coeff = coeff.conj().transpose()
                        Dx[i, i-CLn:i+CLn] = coeff
    
    if spb:
        # If we're making a sparse matrix, convert it now into csr form.
        Dx = Dx.tocsr()
    
    return Dx
## ------