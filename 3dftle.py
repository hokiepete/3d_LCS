# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 12:21:10 2018

@author: pnola
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import scipy.io as sio

from skimage import measure

#f = hp.File('ftle.mat','r')
array = sio.loadmat('ftle.mat')
ftle = array['f'][:,::4,:]
eig1 = array['f'][:,1::4,:]
eig2 = array['f'][:,2::4,:]
eig3 = array['f'][:,3::4,:]
del array
hx=300
hy=300
hz=200
thresh=np.percentile(ftle,98)
import sys
#sys.exit()
dim = ftle.shape
dfdy, dfdx, dfdz = np.gradient(ftle,hy,hx,hz)
dydy, dydx, dydz = np.gradient(dfdy,hy,hx,hz)
dxdy, dxdx, dxdz = np.gradient(dfdx,hy,hx,hz)
dzdy, dzdx, dzdz = np.gradient(dfdz,hy,hx,hz)

dirdiv = np.empty(dim)
concav = np.empty(dim)
for i in range(dim[0]):
    for j in range(dim[1]):
        for k in range(dim[2]):
            dirdiv[i,j,k] = np.dot([dfdx[i,j,k],dfdy[i,j,k],dfdz[i,j,k]],[eig1[i,j,k],eig2[i,j,k],eig3[i,j,k]])
            concav[i,j,k] = np.dot(np.dot([[dxdx[i,j,k],dxdy[i,j,k],dxdz[i,j,k]],[dydx[i,j,k],dydy[i,j,k],dydz[i,j,k]],[dzdx[i,j,k],dzdy[i,j,k],dzdz[i,j,k]]],[eig1[i,j,k],eig2[i,j,k],eig3[i,j,k]]),[eig1[i,j,k],eig2[i,j,k],eig3[i,j,k]])

#dirdiv = np.ma.masked_where(concav>=0,dirdiv)
#dirdiv = np.ma.masked_where(ftle<thresh,dirdiv)

dirdiv[concav>=0]=9999
dirdiv[ftle<thresh]=9999
# Use marching cubes to obtain the surface mesh of these ellipsoids
print "Cube Time"
### marching cubes interprets i as x and j as y
verts, faces, normals, values = measure.marching_cubes_lewiner(volume=dirdiv,level=0,spacing=(hy,hx,hz))
print "Plot Time"
# Display resulting triangular mesh using Matplotlib. This can also be done
# with mayavi (see skimage.measure.marching_cubes_lewiner docstring).
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Fancy indexing: `verts[faces]` to generate a collection of triangles
mesh = Poly3DCollection(verts[faces])
#mesh.set_edgecolor('k')
ax.add_collection3d(mesh)

ax.set_xlim(0, 257*hy)  # a = 6 (times two for 2nd ellipsoid)
ax.set_ylim(0, 259*hx)  # b = 10
ax.set_zlim(0, 41*hz)  # c = 16

### marching cubes interprets i as x and j as y
ax.set_xlabel("S-N")
ax.set_ylabel("w-E")
ax.set_zlabel("U-D")

plt.tight_layout()
plt.savefig('FTLE.png', transparent=True, bbox_inches='tight')
