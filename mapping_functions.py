import numpy

def cot(th):
    return 1.0/numpy.tan(th)

def sec(th):
    return 1.0/numpy.cos(th)

def deg2rad(deg):
    return deg*numpy.pi/180.0

def rad2deg(rad):
    return rad*180.0/numpy.pi
    
def lonlat2km(reflon,reflat,lon,lat ):
    #LONLAT2KM Summary of this function goes here
    #   Uses Lambert Conformal Projection
    stdlat1  =  deg2rad(30)
    stdlat2  =  deg2rad(60)
    R=6371
    reflon = deg2rad(reflon)
    reflat = deg2rad(reflat)
    lon = deg2rad(lon)
    lat = deg2rad(lat)
    n = numpy.log(numpy.cos(stdlat1)*sec(stdlat2)) / numpy.log(numpy.tan(0.25*numpy.pi+0.5*stdlat2)*cot(0.25*numpy.pi+0.5*stdlat1))
    F=(numpy.cos(stdlat1)*(numpy.tan(0.25*numpy.pi+0.5*stdlat1)**n))/n
    p0 = R*F*(cot(0.25*numpy.pi+0.5*reflat)**n)
    p = R*F*(cot(0.25*numpy.pi+0.5*lat)**n)
    th = n*(lon-reflon)
    x=p*numpy.sin(th)
    y=p0-p*numpy.cos(th)
    return x,y

def km2lonlat(reflon,reflat,x,y ):
    #KM2LONLAT Summary of this function goes here
    #   Inverse Lambert Conformal Projection
    stdlat1  =  deg2rad(30)
    stdlat2  =  deg2rad(60)
    R=6371
    reflon = deg2rad(reflon)
    reflat = deg2rad(reflat)
    n = numpy.log(numpy.cos(stdlat1)*sec(stdlat2)) / numpy.log(numpy.tan(0.25*numpy.pi+0.5*stdlat2)*cot(0.25*numpy.pi+0.5*stdlat1))
    F=(numpy.cos(stdlat1)*(numpy.tan(0.25*numpy.pi+0.5*stdlat1)**n))/n
    p0 = R*F*(cot(0.25*numpy.pi+0.5*reflat)**n)
    p = numpy.sign(n)*numpy.sqrt(x**2+(p0-y)**2)
    th = numpy.arctan(x/(p0-y))
    lon = th/n + reflon
    lat = 2*numpy.arctan((R*F/p)**(1/n))-numpy.pi/2
    lon = rad2deg(lon)
    lat = rad2deg(lat)
    return lon,lat