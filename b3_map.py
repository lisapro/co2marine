'''
Created on 15. feb. 2017

@author: ELP
'''

# script creates a map of available 
# data. form WOD, field data, modeling input 

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from netCDF4 import Dataset

#read netcdf from WOD with validation data 
ncfile = 'data_from_Baltic_small_domain_1980.nc'
fh = Dataset(ncfile, mode='r')
lat_odv = fh.variables['latitude'][:]
lon_odv =fh.variables['longitude'][:]


# coordinated of field data with only physics  from Polish institute 
lat = [55.4333, 55.45048333 , 55.5052 ,   
       55.52528333,  55.49421667 ,55.46626667]

lon = [18.15736667,18.14913333, 18.1957,
        18.23168333,18.1884, 18.16268333]

# stations names
stations = [18,23, 4, 7,8,16]

# coordinated of field data with 
# biogeochemical data  from Polish institute 
lat_bgch = [55.5372,55.51843333,55.50116667, 55.52833333, 
            55.5397, 55.50871667, 55.51025,55.48216667,55.45198333,
            55.54351667]

lon_bgch = [18.27465, 18.20873333, 18.23761667,18.20283333,
            18.25776667, 18.2381,18.25151667, 18.17466667,18.17215,
            18.26866667]

st_bgch =  [20,22, 11,1,6,9,10,15,17,19]

# coordinated of TS input from GETM model
b3_getm = [18.1555,55.4863] # E,N 

# coordinates of area with climate relaxation data

lon_relax = [17.55, 19.95] 
lat_relax = [55.00 , 56.50]

#add path to fill rectangle with relax data
from matplotlib.path import Path

verts = [ # define coordinates of rectangle 
    (lon_relax[0], lat_relax[0]),  # P0
    (lon_relax[0], lat_relax[1]), # P1
    (lon_relax[1], lat_relax[1]), # P2
    (lon_relax[1], lat_relax[0])
    ,(lon_relax[0], lat_relax[0]) # P3
    ]

codes = [Path.MOVETO,
         Path.LINETO, # specify the 
         Path.LINETO, # way how to go from 
         Path.LINETO, # one point to another
         Path.LINETO, # it can be filled only with 
         ] # LINETO

path = Path(verts, codes)

# add figure
fig, ax  = plt.subplots(figsize=(8.27, 10 ), dpi=100 )

ax.set_title('Available data for B3 field')
#ax.scatter(lon,lat, label='hydrological, biological sampling', zorder = 6)
ax.scatter(lon_bgch, lat_bgch, zorder = 6,
            label='hydrological, geochemical, biological sampling', s = 10)
ax.scatter(b3_getm[0],b3_getm[1], label='model T,S, input data ',
            s = 100, zorder = 5)
ax.scatter(lon_odv,lat_odv, label='Valdiation data from WOD', color = '#cccccc', zorder = 2)

patch = patches.PathPatch(path, facecolor='#b7ebd9', lw=1,alpha = 0.1)
ax.add_patch(patch)

xs, ys = zip(*verts)
ax.plot(xs, ys,  lw=2, color='#b7ebd9', ms= False,label='Climate relaxation data ', zorder = 1)



ax.plot()
ax.annotate('GETM\ninput',(b3_getm[0],b3_getm[1]),xytext=(-10, 5),
                ha='right', va='bottom',textcoords='offset points', zorder = 10)

# can be added to plot numbers of stations 
# removed it because of small scale
'''for i, txt in enumerate(stations):
    ax.annotate(txt, (lon[i],lat[i]),xytext=(17, 0),
                ha='right', va='bottom',textcoords='offset points'  )
    
for i, txt in enumerate(st_bgch):
    ax.annotate(txt, (lon_bgch[i],lat_bgch[i]),xytext=(17, 0),
                ha='right', va='bottom',textcoords='offset points'  )  ''' 
    
legend = ax.legend( shadow=False, loc='best') #bbox_to_anchor=(0.8, 0.35))       

plt.show()





