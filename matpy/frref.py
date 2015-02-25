import numpy as np
import numpy.linalg as nlg
import scipy
import scipy.sparse as sp
import scipy.linalg as splg

def frref(A, tol = 1e-10):
    m = A.shape[0]
    n = A.shape[1]
    
    if sp.issparse(A):
        use_sparse = True
        r = nlg.qr(A.todense(), mode = 'r')
    else:
        use_sparse = False
        r = nlg.qr(A, mode = 'r')
    print(r)

    r[abs(r) < tol] = 0

    indep_rows = (r!=0).max(axis=1)
    indep_rows = np.ravel(indep_rows)

    i_dep = np.nonzero(indep_rows)[0]
    i_indep = np.nonzero(1-indep_rows)[0]

    L_indep = np.min(i_indep.shape)
    L_dep   = np.min(i_dep.shape)

    indep_rows = np.arange(len(indep_rows))[indep_rows]

    F = sp.lil_matrix((m,n))
    
    if L_indep != 0:
        tmp = nlg.lstsq(r[indep_rows,:][:,i_dep],\
                        r[indep_rows,:][:,i_indep])[0]

        ii,jj = np.meshgrid(indep_rows,i_indep)

        F[np.ravel(ii),np.ravel(jj)] = np.ravel(tmp)
    
    if L_dep != 0:
        F[indep_rows,i_dep] = np.ones(L_dep)
    
    if use_sparse:
        F.tocsr()
    else:
        F = F.todense()
    
    return F


if __name__ == '__main__':

    X1 = np.array([[1,1,0],[1,1,0],[0,0,1]])
    X2 = np.array([[1,2,3],[1,2,4],[3,2,1]])
    X3 = np.array([[1.,2.,3.],[1.,2.,3.],[3.,2.,1.]])

    X4 = sp.lil_matrix((10,10))
    X4[0,0:2]  = [1,1]
    X4[1,0:2]  = [1,1]
    X4[2,2]    = 1
    X4[3,1:4]  = [1,2,3]
    X4[4,2:5]  = [1,2,3]
    X4[5,3:6]  = [1,2,3]
    X4[6,4:7]  = [1,2,3]
    X4[7,5:8]  = [1,2,3]
    X4[8,6:9]  = [1,2,3]
    X4[9,7:10] = [1,2,3]

    np.set_printoptions(precision=3)

    Y1 = frref(X1)
    print('X1 -> Y1')
    print(X1)
    print(Y1)

    Y2 = frref(X2)
    print('X2 -> Y2')
    print(X2)
    print(Y2)

    Y3 = frref(X3)
    print('X3 -> Y3')
    print(X3)
    print(Y3)

    Y4 = frref(X4)
    print('X4 -> Y4')
    print(X4.todense())
    print(Y4.todense())


