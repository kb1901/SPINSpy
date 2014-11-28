import matplotlib.cm as colmap
import matplotlib.colors as mplc
import matplotlib.pyplot as plt
import numpy as np

## Create DarkJet
## ------
col_list = colmap.jet(range(256))
darken = np.tile((1 - 0.5/np.cosh(np.linspace(-10,10,256))).reshape((256,1)), [1,col_list.shape[1]])
darkjet = mplc.ListedColormap(col_list*darken, 'darkjet', 256)
plt.register_cmap(cmap=darkjet)
## ------