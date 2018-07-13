
#Domain [-300 300]^2 km
#Origin (41.3209371228N, 289.46309961W)
#Projection Lambert
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import h5py as hp
import mapping_functions as mf
cdict = {'red':  [(0.0, 0.0000, 0.0000),
                  (0.5, 1.0000, 1.0000),
                  (1.0, 1.0000, 1.0000)],
        'green': [(0.0, 0.5450, 0.5450),
                  (0.5, 1.0000, 1.0000),
                  (1.0, 0.5450, 0.5450)],
        'blue':  [(0.0, 0.5450, 0.5450),
                  (0.5, 1.0000, 1.0000),
                  (1.0, 0.0000, 0.0000)]}
plt.register_cmap(name='CyanOrange', data=cdict)
plt.close('all')
#origin = [41.3209371228, 289.46309961]
Lat = 37.208
Lon =-80.5803

origin = [37.208,-80.5803]
# setup lambert conformal basemap.
# lat_1 is first standard parallel.
# lat_2 is second standard parallel (defaults to lat_1).
# lon_0,lat_0 is central point.
# rsphere=(6378137.00,6356752.3142) specifies WGS84 ellipsoid
# area_thresh=1000 means don't plot coastline features less
# than 1000 km^2 in area.
#'''

lllon, lllat = mf.km2lonlat(Lon,Lat,-77400/2000.0,-76800/2000.0)
urlon, urlat = mf.km2lonlat(Lon,Lat,77400/2000.0,76800/2000.0)

'''
m = Basemap(width=77400,height=76800,
            rsphere=(6378137.00,6356752.3142),\
            resolution='f',area_thresh=0.,projection='lcc',\
            lat_1=35.,lat_0=origin[0],lon_0=origin[1],epsg=2284)
m = Basemap(rsphere=(6378137.00,6356752.3142),\
            llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon,\
            resolution='f',area_thresh=0.,projection='lcc',\
            lat_1=35.,lat_0=origin[0],lon_0=origin[1],epsg=2284)
'''
m = Basemap(rsphere=(6378137.00,6356752.3142),\
            llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon,\
            projection='lcc',\
            epsg=2284)
width =7
fig = plt.figure(1,figsize=(width,0.992*width))
#'''
#epsg=3687)
#2925
#2854
#2284
#m.drawparallels(np.arange(35,39,0.15),labels=[True,False,False,False])
#m.drawmeridians(np.arange(-82,-78,0.15),labels=[False,False,False,True])
m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 3000, verbose= True)
#m.warpimage(image=m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2000, verbose= True))
'''
m.drawcoastlines()
m.drawrivers()
m.drawstates()
m.fillcontinents(lake_color='b')
#'''
#m.bluemarble()
#m.etopo()
plt.tight_layout()
plt.savefig('Map.png', transparent=True, bbox_inches='tight',pad_inches=0)