'''
Created on 6. feb. 2017

@author: ELP
'''
# Script reads Netcdf file with GETM output and WOD data for chosen region 
# It Plots vertical profiles of Temperature for each day from GETM
# And vertical profiles of Temperature for each station at WOD
# It calculates and plots the year average profile for GETM and WOD data 
# 

import pdb #python debugger 
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
#from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger
from matplotlib.pyplot import axes
plt.style.use('ggplot')

def read_netcdf_odv(ncfile):

    fh = Dataset(ncfile, mode='r')
    date_time = fh.variables['date_time'][:]
    #depth = fh.variables['var1'][:][:]
    depthmasked = fh.variables['var1'][:][:]
    depth = depthmasked.filled(fill_value= np.nan)    
    depth2 = fh.variables['var1'][:][:]
    tempmasked = fh.variables['var2'][:][:]
    temp = tempmasked.filled(fill_value= np.nan)   
                                 
    fh.close()

    dates1 = num2date(date_time[:],units='days since 1990-01-01',
                 calendar='proleptic_gregorian' )
    
    return depth,temp


ncfile = 'data_from_OSD_small domain.nc'

# Call the function reading netcdf file with data from WOD 
w = read_netcdf_odv(ncfile)
temp = w[1] 
depth = w[0]

length = (len(temp))
temp_int = []
# Interpolate temperature to standard depths
for n in range(0,length):
    f = interpolate.interp1d(depth[n],temp[n],bounds_error=False, fill_value=np.nan)
    ynew = np.arange(0,100, 5) #Define standard depths 
    xnew = f(ynew)   # use interpolation function returned by `interp1d`
    temp_int.append(xnew)


means = []  
#transpose the interpolated array   
temp_int_t = (np.array(temp_int)).T

#Calulate the mean for each level 
for n in range(0,len(temp_int_t)):
    m = np.nanmean(temp_int_t[n])
    means.append(m)  

# Open NetCDF file with GETM data 
fh2 = Dataset('B3zax-kz.nc')
dd = np.array(fh2.variables['zax'][:])   #read depths 
depth_getm = dd * -1 # change the y axis direction 
tt = np.ravel(fh2.variables['temp'][:])    
temp_getm = np.reshape(tt,(7670,78))  
temp_getm_t = temp_getm.transpose()

    
dates = [datetime.datetime(1990,1,1)+n* # (1990,1,1) is a starting point for  
         timedelta(days=365) for n in range(22)]  # time calculation in the array 
y = date2num(dates, units = 'days since 1990-01-01',
                 calendar= 'proleptic_gregorian') 

# create the pdf file for storing pictures 
with PdfPages('Temp_GETM.pdf') as pdf: 
    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    ax00 = figure.add_subplot(gs[0]) # water 
    ax01 = figure.add_subplot(gs[1], sharex=ax00) # water 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) # water 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) # water 

    axes_list = (ax00,ax01,ax02,ax03)   
    
    def title(axis,year):    
        axis.set_title('year {} '.format(year))
        
    for n in range(0,4):   
        title(axes_list[n],dates[n])
        axes_list[n].set_ylim(100,0)
                
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[0]):int(y[1])])
        means_getm.append(m)       
               
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)   
                      
    for n in range(0,length,1): #field data
        ax00.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')             
    for m in range(0,int(y[1]),1): #1990
        ax00.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')  


    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[1]):int(y[2])])
        means_getm.append(m)     
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)             
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)  
         
    for n in range(0,length,1): #field data        
        ax01.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')       
    for m in range(int(y[1]),int(y[2]),1): #1991
        ax01.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[2]):int(y[3])])
        means_getm.append(m)     
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)                  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)  
                
    for n in range(0,length,1): 
        ax02.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')            
    for m in range(int(y[2]),int(y[3]),1): #1992
        ax02.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')     
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[3]):int(y[4])])
        means_getm.append(m)     
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)     
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)          
    for n in range(0,length,1): #field data
        ax03.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')            
    for m in range(int(y[3]),int(y[4]),1): #1993
        ax03.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    pdf.savefig()
    plt.close()   
    
    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    
    ax00 = figure.add_subplot(gs[0]) # water 
    ax01 = figure.add_subplot(gs[1], sharex=ax00) 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) 
    ax03 = figure.add_subplot(gs[3], sharex=ax00)     
    axes_list = (ax00,ax01,ax02,ax03)   
       
    for n in range(0,4):   
        title(axes_list[n],dates[n+4])
        axes_list[n].set_ylim(100,0)
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[4]):int(y[5])])
        means_getm.append(m)                      
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
               
    for n in range(0,length,1): #field data
        ax00.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[4]),int(y[5]),1): #1990
        ax00.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')


    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[5]):int(y[6])])
        means_getm.append(m)                      
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
          
    for n in range(0,length,1): #field data
        ax01.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[5]),int(y[6]),1):
        ax01.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[6]):int(y[7])])
        means_getm.append(m)                      
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
    for n in range(0,length,1): #field data
        ax02.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')          
    for m in range(int(y[6]),int(y[7]),1):
        ax02.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[7]):int(y[8])])
        means_getm.append(m)                      
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)   
            
    for n in range(0,length,1): #field data
        ax03.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[7]),int(y[8]),1): 
        ax03.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')    
    
    
    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    plt.close()  
    
    
    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    
    ax00 = figure.add_subplot(gs[0])  
    ax01 = figure.add_subplot(gs[1], sharex=ax00) 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) 
    ax03 = figure.add_subplot(gs[3], sharex=ax00)      
    axes_list = (ax00,ax01,ax02,ax03)  
       
    for n in range(0,4):   
        title(axes_list[n],dates[n+8])
        axes_list[n].set_ylim(100,0)

    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[8]):int(y[9])])
        means_getm.append(m)                      
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
        
    for n in range(0,length,1): #field data
        ax00.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[8]),int(y[9]),1): #1990
        ax00.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[9]):int(y[10])])
        means_getm.append(m)                      
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
    
            
    for n in range(0,length,1): #field data
        ax01.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')          
    for m in range(int(y[9]),int(y[10]),1):
        ax01.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[10]):int(y[11])])
        means_getm.append(m)                      
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
                
    for n in range(0,length,1): #field data
        ax02.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[10]),int(y[11]),1):
        ax02.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[11]):int(y[12])])
        means_getm.append(m)                      
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
    
            
    for n in range(0,length,1): #field data
        ax03.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[11]),int(y[12]),1): 
        ax03.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')    
    

    
    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    plt.close()     
    
    
    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    
    ax00 = figure.add_subplot(gs[0]) # water 
    ax01 = figure.add_subplot(gs[1], sharex=ax00) # water 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) # water 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) # water       
    axes_list = (ax00,ax01,ax02,ax03) #,ax04,ax05    
       
    for n in range(0,4):   
        title(axes_list[n],dates[n+12])# #print (y[n])
        axes_list[n].set_ylim(100,0)
        
        means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[12]):int(y[13])])
        means_getm.append(m)                      
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
        
    for n in range(0,length,1): #field data
        ax00.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[12]),int(y[13]),1): #1990
        ax00.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')  
        
        means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[13]):int(y[14])])
        means_getm.append(m)                      
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)    
        
    for n in range(0,length,1): #field data
        ax01.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[13]),int(y[14]),1):
        ax01.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[14]):int(y[15])])
        means_getm.append(m)                      
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
         
    for n in range(0,length,1): #field data
        ax02.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[14]),int(y[15]),1):
        ax02.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[15]):int(y[16])])
        means_getm.append(m)                      
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
            
    for n in range(0,length,1): #field data
        ax03.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[15]),int(y[16]),1): 
        ax03.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')    
    

    
    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    plt.close()     


    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    
    ax00 = figure.add_subplot(gs[0]) # water 
    ax01 = figure.add_subplot(gs[1], sharex=ax00) # water 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) # water 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) # water       
    axes_list = (ax00,ax01,ax02,ax03) #,ax04,ax05    
       
    for n in range(0,4):   
        title(axes_list[n],dates[n+16])# #print (y[n])
        axes_list[n].set_ylim(100,0)
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[16]):int(y[17])])
        means_getm.append(m)                      
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
    for n in range(0,length,1): #field data
        ax00.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[16]),int(y[17]),1): #1990
        ax00.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[17]):int(y[18])])
        means_getm.append(m)                      
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
    for n in range(0,length,1): #field data
        ax01.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')           
    for m in range(int(y[17]),int(y[18]),1):
        ax01.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[18]):int(y[19])])
        means_getm.append(m)                      
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
        
    for n in range(0,length,1): #field data
        ax02.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')          
    for m in range(int(y[18]),int(y[19]),1):
        ax02.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
        
    means_getm = []
    for n in range(0,len(temp_getm_t)):
        m = np.nanmean(temp_getm_t[n][int(y[19]):int(y[20])])
        means_getm.append(m)                      
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
    for n in range(0,length,1): #field data
        ax03.plot(temp[n],depth[n],linewidth = 0.2,color ='#7dadbc')          
    for m in range(int(y[19]),int(y[20]),1): 
        ax03.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807')      
    
    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    plt.close()          

  
        