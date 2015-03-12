import numpy as np
import numpy.linalg as nlg
import scipy
import scipy.sparse as sp
import scipy.linalg as splg

def frref(A, tol = 1e-20):
    m = A.shape[0]
    n = A.shape[1]
    
    if sp.issparse(A):
        use_sparse = True
        r = splg.qr(A.todense(), mode = 'r')
    else:
        use_sparse = False
        r = splg.qr(A, mode = 'r')[0]
        #r = splg.qr(A, mode = 'r', pivoting=True)[0]
        #r = nlg.qr(A, mode = 'r')

    r[np.abs(r) < tol] = 0
    #print(r)

    np.set_printoptions(linewidth=200)
    tmp = np.argmax(np.abs(r) > tol, axis=1)

    indep_rows = (np.abs(r) > tol).max(axis=1)
    indep_rows = np.ravel(indep_rows)

    i_dep   = tmp[indep_rows]
    i_dep   = np.unique(i_dep)
    i_indep = np.setdiff1d(np.arange(n), i_dep)

    #print(i_dep)
    #print(i_indep)

    L_indep = len(i_indep)
    L_dep   = len(i_dep)

    #print(indep_rows)
    indep_rows = np.arange(len(indep_rows))[indep_rows]
    #print(indep_rows)

    # When there are more elements than conditions.
    # we need to add some `filler' conditions. 
    if n < m:
        F = sp.lil_matrix((m,n))
    else:
        F = sp.lil_matrix((n,n))
    #print(F.shape, A.shape, r.shape)
    
    if L_indep != 0:
        lf = r[indep_rows,:][:,i_dep]
        rg = r[indep_rows,:][:,i_indep]

        #print(lf)
        #print(rg)

        tmp = nlg.lstsq(r[indep_rows,:][:,i_dep],\
                        r[indep_rows,:][:,i_indep])[0]
        ii,jj = np.meshgrid(i_dep,i_indep)

        #print(ii.ravel().shape)
        #print(jj.ravel().shape)
        #print(tmp.shape)
        F[np.ravel(ii),np.ravel(jj)] = np.ravel(tmp)
    
    if L_dep != 0:
        F[i_dep,i_dep] = np.ones(L_dep)

    #print(F.todense())
    # Now remove some of the `filler' conditions
    if n > m:
        nz_row,nz_col = F.nonzero()
        nz_row = np.unique(nz_row)
        nz_row = np.setdiff1d(np.arange(n), nz_row)
        nz_row = nz_row[0:n-m]
        #print(nz_row)
        delete_row_lil(F,nz_row)

    if use_sparse:
        F.tocsr()
    else:
        F = F.todense()
   
    #print(F)
    return F

# Define a function that deletes rows from sparse LIL matrices
def delete_row_lil(mat, inds):
    if not isinstance(mat, scipy.sparse.lil_matrix):
        raise ValueError("works only for LIL format -- use .tolil() first")

    if isinstance(inds, type(np.zeros((2,2)))):
        # Sort the indices to be careful
        inds = inds.ravel()
        inds.sort()
        inds[:] = inds[::-1]
        for i in inds:
            mat.rows = np.delete(mat.rows, i)
            mat.data = np.delete(mat.data, i)
            mat._shape = (mat._shape[0] - 1, mat._shape[1])
    elif isinstance(inds, type([0])):
        # Sort to be careful
        inds.sort()
        inds[:] = inds[::-1]
        for i in inds:
            mat.rows = np.delete(mat.rows, i)
            mat.data = np.delete(mat.data, i)
            mat._shape = (mat._shape[0] - 1, mat._shape[1])
    elif isinstance(inds, type(1)):
        mat.rows = np.delete(mat.rows, i)
        mat.data = np.delete(mat.data, i)
        mat._shape = (mat._shape[0] - 1, mat._shape[1])
    else:
        raise ValueError("inds must either be an integer, list, or 1D numpy array")


if __name__ == '__main__':

    X1 = np.array([[1,1,0],[1,1,0],[0,0,1]])
    X2 = np.array([[1,2,3],[1,2,4],[3,2,1]])
    X3 = np.array([[1.,2.,3.],[1.,2.,3.],[3.,2.,1.]])


    X4 = np.array([[ 0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.],
                   [ 0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.],
                   [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.],
                   [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                   [ 0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.],
                   [ 0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.],
                   [ 0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.],
                   [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.],
                   [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.],
                   [ 1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                   [ 0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                   [ 0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.]])

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
    print(X4)
    print(Y4)


