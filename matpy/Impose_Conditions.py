import numpy as np
import scipy
import scipy.sparse as sp
import sys
from frref import frref

def Impose_Conditions(bs, tol = 1e-20):
# IMPOSE_CONDITIONS imposes arbitrary linear and homogenous conditions
# on a matrix A.
# > bs is an MxN matrix, where each row corresponds to a condition of the form
#   bs(ii,:) /dot /vec{x} = 0.
# > M must be strictly less than N.
# > A warning message will be printed for any redundant conditions.
# > Output As contains, in the same order as input As, the input matrices
#   with the conditions of bs applied.
# > P is the transfromation matrix. That is, if P = Impose_Conditions(bs),
#   then solving [eigvec, eigval] = eig(P\A*P) solves the constrained
#   problem. P*eigvec re-introduces any points that may have been removed 
#   in order to impose the constraints.

    ## Step 1: Row reduce the problem to make sure that we don't have
    #          linearly dependent conditions.
  
    num_conds, num_elems = bs.shape

    np.set_printoptions(linewidth=350, precision=1)

    print(bs)
    bs = np.asarray(frref(bs))
    print(bs)

    tmp = np.arange(num_conds)[np.ravel(np.sum(np.abs(bs),axis=1) > tol)]
    print(tmp)
    bs = bs[tmp,:]
  
    if num_conds > bs.shape[0]:
        null_conds = num_conds - bs.shape[0]
        num_conds = bs.shape[0]
        print('Impose_Conditions: {0:d} Conditions were '.format(null_conds) + \
              'linear combinations of the other conditions.' + \
              ' There are {0:d} conditions remaining.'.format(num_conds))
    
    ## Step 2: Check inputs    
    if bs.shape[0] > bs.shape[1]:
        print('Impose_Conditions: System is over-defined.')
	sys.exit()
    elif bs.shape[0] == bs.shape[1]:
        print('Impose_Conditions: System is critically defined and could be found uniquely.')
        sys.exit()

    ## Step 3: Impose the conditions
  
    # First, find the indices of the removed points
    # That is, find the column index for the leading
    # one in each row.
    removed_indices = np.argmax(np.abs(bs) > 0.5, axis=1)
    sort_inds = np.argsort(np.ravel(removed_indices))
    removed_indices = np.ravel(removed_indices[sort_inds])
    bs = bs[sort_inds,:]
  
    # Now reduce the bs matrix
    bs = np.delete(bs,removed_indices,axis=1)
    cnt = np.count_nonzero(np.abs(bs) > tol)
    meta_ind = np.arange(bs.shape[1])
     
    # Initialize the transformation matrix P
    ind1 = np.zeros(cnt+num_elems-num_conds)
    ind2 = np.zeros(cnt+num_elems-num_conds)
    vals = np.zeros(cnt+num_elems-num_conds)
    #print(ind1.shape)
    #print(cnt,num_elems,num_conds)
    
    # Now find the index-value arrangement for the transformation matrix P
    ind = 0 # To keep track of how many removed points we've reconstructed.
    tracker = 0 # To keep track of where we are in ind1, ind2, and vals.
    for ii in range(num_elems):
        #print(ii,tracker)
        # We loop through, computing the reconstruction vector for each
        # point. That is, x_i in x_original = v .* x_reduced. Here we
        # determine v.
        if ind < len(removed_indices) and ii == removed_indices[ind]:
            # If we're reconstructing one of the removed points...

            # Find the index for any points needed for the reconstruction
            sel = np.arange(bs.shape[1])[np.ravel(np.abs(bs[ind,:])>tol)]
            print(sel)
            
            # If there weren't any, then it's just zero.
            if len(sel) == 0:
                ind += 1

                # If there were some, record it.
            else:
                tmp_ind = meta_ind[sel]
                if len(sel) == 1:
                    tmp_ind = np.array([tmp_ind])

                leng = len(tmp_ind) # How many other points are needed for the 
                                    # reconstruction
                ind1[tracker:tracker+leng] = ii
                ind2[tracker:tracker+leng] = tmp_ind
                vals[tracker:tracker+leng] = bs[ind,tmp_ind]
                tracker += leng
                ind += 1
        else:
            # If we're reconstructing a point that wasn't removed, then it's
            # really easy.
            ind1[tracker] = ii # We're returning the ii^th element
            ind2[tracker] = ii - ind     # But in the reduced vector, it's 
                                         # (ii-ind+1)^st element
            vals[tracker] = 1
            tracker += 1
    
    #print(vals)
    #print(ind1)
    #print(ind2)

    P = sp.csr_matrix((vals, (ind1, ind2)), shape=(num_elems,num_elems-num_conds))
    #print(P.shape)
    #print(P.todense())
 
    return P
