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
from skimage.draw import ellipsoid

#f = hp.File('ftle.mat','r')
array = sio.loadmat('ftle.mat')
ftle = array['f'][:,::4,:]
eig1 = array['f'][:,1::4,:]
eig2 = array['f'][:,2::4,:]
eig3 = array['f'][:,3::4,:]
del array

dim = ftle.shape
dfdy, dfdx, dfdz = np.gradient(ftle)
dydy, dydx, dydz = np.gradient(dfdy)
dxdy, dxdx, dxdz = np.gradient(dfdx)
dzdy, dzdx, dzdz = np.gradient(dfdz)

dirdiv = np.empty(dim)
concav = np.empty(dim)
for i in range(dim[0]):
    for j in range(dim[1]):
        for k in range(dim[2]):
            dirdiv[i,j,k] = np.dot([dfdx[i,j,k],dfdy[i,j,k],dfdz[i,j,k]],[eig1[i,j,k],eig2[i,j,k],eig3[i,j,k]])
            concav[i,j,k] = np.dot(np.dot([[dxdx[i,j,k],dxdy[i,j,k],dxdz[i,j,k]],[dydx[i,j,k],dydy[i,j,k],dydz[i,j,k]],[dzdx[i,j,k],dzdy[i,j,k],dzdz[i,j,k]]],[eig1[i,j,k],eig2[i,j,k],eig3[i,j,k]]),[eig1[i,j,k],eig2[i,j,k],eig3[i,j,k]])

dirdiv = np.ma.masked_where(concav>=0,dirdiv)
'''
# Generate a level set about zero of two identical ellipsoids in 3D
ellip_base = ellipsoid(6, 10, 16, levelset=True)
ellip_double = np.concatenate((ellip_base[:-1, ...],
                              ellip_base[2:, ...]), axis=0)
'''
# Use marching cubes to obtain the surface mesh of these ellipsoids
print "Plot Time"
verts, faces, normals, values = measure.marching_cubes_lewiner(dirdiv, 0)
#verts, faces, normals, values = measure.marching_cubes_lewiner(ellip_double, 0)

# Display resulting triangular mesh using Matplotlib. This can also be done
# with mayavi (see skimage.measure.marching_cubes_lewiner docstring).
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Fancy indexing: `verts[faces]` to generate a collection of triangles
mesh = Poly3DCollection(verts[faces])
mesh.set_edgecolor('k')
ax.add_collection3d(mesh)

ax.set_xlabel("x-axis: a = 6 per ellipsoid")
ax.set_ylabel("y-axis: b = 10")
ax.set_zlabel("z-axis: c = 16")

ax.set_xlim(0, 258)  # a = 6 (times two for 2nd ellipsoid)
ax.set_ylim(0, 256)  # b = 10
ax.set_zlim(0, 40)  # c = 16

plt.tight_layout()
plt.savefig('FTLE.png', transparent=True, bbox_inches='tight')
#plt.show()