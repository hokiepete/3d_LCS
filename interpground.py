import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.io import savemat
Data = np.load('NAMdata0000.npz')
ground = Data['arr_0'][3]
xinlim = (ground.shape[1]-1)*3000/2.0
yinlim = (ground.shape[0]-1)*3000/2.0
xoutlim = 258*300/2.0
youtlim = 256*300/2.0
xin = np.linspace(-xinlim,xinlim,ground.shape[1])
yin = np.linspace(-yinlim,yinlim,ground.shape[0])
#xin,yin = np.meshgrid(x,y)
xout = np.linspace(-xoutlim,xoutlim,670)
yout = np.linspace(-youtlim,youtlim,633)
#xout,yout = np.meshgrid(x,y)
ground_func = RectBivariateSpline(yin,xin,ground)
groundout = ground_func(yout,xout)
savemat('grounddata.mat',{'ground':groundout})
