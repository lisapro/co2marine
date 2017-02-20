'''
Created on 6. feb. 2017

@author: ELP
'''


from datetime import datetime, timedelta,date
from netCDF4 import Dataset 
from netCDF4 import num2date, date2num
import numpy.ma as ma
import numpy as np
from scipy import interpolate
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pandas as pd
from  matplotlib.backends.backend_pdf import PdfPages
import pylab
import matplotlib.gridspec as gridspec
import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger
from matplotlib.pyplot import axes
plt.style.use('ggplot')


ncfile = 'data_from_Baltic_small_domain_1980.nc'
#ncfile = 'data_from_OSD_small domain.nc'
fh = Dataset(ncfile, mode='r')

date_time = fh.variables['date_time'][:]
#depth = fh.variables['var1'][:][:]
depthmasked = fh.variables['var1'][:][:]
depth = depthmasked.filled(fill_value= np.nan)    
depth2 = fh.variables['var1'][:][:]

tempmasked = fh.variables['var2'][:][:]
temp = tempmasked.filled(fill_value= np.nan)   

                                 
fh.close()

dates1 = num2date(date_time[:],units='days since 1980-01-01',
             calendar='proleptic_gregorian' )

length = (len(temp))
ym = np.arange(1,80,5)
m = interpolate.interp1d(temp[0], depth[0],
            assume_sorted=True)

import matplotlib.pyplot as plt
from scipy import interpolate
figure = plt.figure()

gs = gridspec.GridSpec(1,2)
ax = figure.add_subplot(gs[0]) # water    
ax1 = figure.add_subplot(gs[1]) # water    
ax.set_ylim(100,-1)
ax1.set_ylim(100,-1)
ax.set_title('interpolated')
ax1.set_title('raw')

#x = np.arange(0, 10)
#y = np.arange(0, 100,10)
temp_int = []
for n in range(0,length):
    f = interpolate.interp1d(depth[n],temp[n],bounds_error=False, fill_value=np.nan)
    ynew = np.arange(0,100, 5)
    xnew = f(ynew)   # use interpolation function returned by `interp1d`
    temp_int.append(xnew)
    ax.plot( xnew, ynew, 'o',markersize = 3)
    #ax1.plot(temp[n], depth[n], 'o',markersize = 3)    
#gs.update(wspace=0.3,hspace = 0.4)



means = []    
temp_int_t = (np.array(temp_int)).T

for n in range(0,len(temp_int_t)):
    m = np.nanmean(temp_int_t[n])
    means.append(m)  
#m = np.nanmean(temp_int_t[0])
#print(m)


'''    
fh2 = Dataset('B3zax-kz.nc')
dd = np.array(fh2.variables['zax'][:])   
depth_getm = dd * -1
tt = np.ravel(fh2.variables['temp'][:])    
temp_getm = np.reshape(tt,(7670,78))
temp_getm_t = temp_getm.transpose()

dates = [datetime.datetime(1990,1,1)+n*
         timedelta(days=365) for n in range(22)]  
y = date2num(dates, units = 'days since 1990-01-01',
                 calendar= 'proleptic_gregorian')


means_getm = []
for n in range(0,len(temp_getm_t)):
    m = np.nanmean(temp_getm_t[n][int(y[0]):int(y[1])])
    means_getm.append(m)      
'''

#ax.plot(means,ynew,zorder = 10,
#          marker = 'o', color = 'k', markersize = 4)   
#ax.plot(means_getm,depth_getm,zorder = 10,
#          marker = 'o', color = 'c', markersize = 2)   
plt.show()



