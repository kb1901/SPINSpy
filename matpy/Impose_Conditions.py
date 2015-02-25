import numpy as np
import scipy
import scipy.sparse as sp
import sys
from frref import frref

def Impose_Conditions(bs, tol = 1e-10)
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

    ## Step 1: Check inputs    
    if bs.shape[0] > bs.shape[1]
        print('Impose_Conditions: System is over-defined.')
	sys.exit()
    elif bs.shape[0] == bs.shape[1]
        print('Impose_Conditions: System is critically defined and could be found uniquely.')
        sys.exit()

    ## Step 2: Row reduce the problem to make sure that we don't have
    #          linearly dependent conditions.
  
    num_conds, num_elems = bs.shape
  
    bs = frref(bs)
    tmp = np.arange(num_conds)[np.sum(np.abs(bs),axis=1)~=0]
    bs = bs(tmp,:)
  
    if num_conds > bs.shape[0]
        null_conds = num_conds - size(bs,1)
        num_conds = size(bs,1)
        print('Impose_Conditions: {0:d} Conditions were '.format(null_conds) + \
              'linear combinations of the other conditions.' + \
              ' There are {0:d} conditions remaining.'.format(num_conds))
    
    ## Step 3: Impose the conditions
  
    # First, find the indices of the removed points
    # That is, find the column index for the leading
    # one in each row.
    removed_indices = np.argmax(abs(bs) > 0.5, axis=1)
    sort_inds = np.argsort(removed_indices)
    #removed_indices = removed_indices(sort_inds)
    bs = bs(sort_inds,:)
  
    # Now reduce the bs matrix
    bs = np.delete(bs,removed_indices,axis=1)
    cnt = np.count_nonzero(abs(bs) > tol)
    meta_ind = range(bs.shape[1])
  
    # Initialize the transformation matrix P
    ind1 = np.zeros(cnt+num_elems-num_conds)
    ind2 = np.zeros(cnt+num_elems-num_conds)
    vals = mp.zeros(cnt+num_elems-num_conds) 
  
    # Now find the index-value arrangement for the transformation matrix P
    ind = 1; # To keep track of how many removed points we've reconstructed.
    tracker = 1; % To keep track of where we are in ind1, ind2, and vals.
    for ii = 1:num_elems
        # We loop through, computing the reconstruction vector for each
        # point. That is, x_i in x_original = v .* x_reduced. Here we
        # determine v.
        if ii == removed_indices(ind)
            # If we're reconstructing one of the removed points...
            #tmp_ind = find(bs(ind,:));
            tmp_ind = meta_ind(bs(ind,:)~=0);
            len = length(tmp_ind); # How many other points are needed for the 
                                   # reconstruction
            ind1(tracker:tracker+len-1) = ii;
            ind2(tracker:tracker+len-1) = tmp_ind;
            vals(tracker:tracker+len-1) = bs(ind,tmp_ind);
            tracker = tracker + len;
            ind = ind + 1;
          
        else
            # If we're reconstructing a point that wasn't removed, then it's
            # really easy.
            ind1(tracker) = ii; # We're returning the ii^th element
            ind2(tracker) = ii - ind + 1; # But in the reduced vector, it's 
                                          # (ii-ind+1)^st element
            vals(tracker) = 1;
            tracker = tracker + 1;
  
    P = sp.csr_matrix((vals, (ind1, ind2)))
 
    return P
