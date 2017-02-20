'''
Created on 7. feb. 2017

@author: ELP
'''

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
from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger
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
    # read data (which is storde in masked array) from netcdf file 
    salmasked = fh.variables['var3'][:][:]   
    # change tha value of mask to nan 
    sal = salmasked.filled(fill_value= np.nan)      
                                 
    fh.close()

    #dates1 = num2date(date_time[:],units='days since 1990-01-01',
    #             calendar='proleptic_gregorian' )
    
    return depth,temp,sal#,sal,o2,po4,si,no3,no2,pH,chl,dates,alk,depth2

ncfile = 'data_from_Baltic_small_domain_1980.nc'
w = read_netcdf_odv(ncfile)

depth = w[0]
temp = w[1] 
sal = w[2]

length = (len(sal))
sal_int = []
for n in range(0,length):
    f = interpolate.interp1d(depth[n],sal[n],bounds_error=False, fill_value=np.nan)
    ynew = np.arange(0,100, 5)
    xnew = f(ynew)   # use interpolation function returned by `interp1d`
    sal_int.append(xnew)
    #ax.plot( xnew, ynew, 'o',markersize = 3)
    #ax1.plot(sal[n], depth[n], 'o',markersize = 3)    
    #gs.update(wspace=0.3,hspace = 0.4)

means = []    
sal_int_t = (np.array(sal_int)).T
for n in range(0,len(sal_int_t)):
    m = np.nanmean(sal_int_t[n])
    means.append(m)  

fh2 = Dataset('B3zax-kz.nc')
dd = np.array(fh2.variables['zax'][:])   
depth_getm = dd * -1
tt = np.ravel(fh2.variables['salt'][:])    
sal_getm = np.reshape(tt,(7670,78))
sal_getm_t = sal_getm.transpose()

    
dates = [datetime.datetime(1990,1,1)+n*
         timedelta(days=365) for n in range(22)]  

years = ['1990','1991','1992','1993','1994','1995','1996','1997',
         '1998','1999','2000','2001','2002','2003','2004','2005',
         '2006','2007','2008','2009','2010']

y = date2num(dates, units = 'days since 1990-01-01',
                 calendar= 'proleptic_gregorian') 

with PdfPages('Sal_GETM.pdf') as pdf:
    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    figure.suptitle('Salinity', fontsize=16)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    ax00 = figure.add_subplot(gs[0]) # water 
    
    ax01 = figure.add_subplot(gs[1], sharex=ax00) # water 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) # water 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) # water 

    axes_list = (ax00,ax01,ax02,ax03) #,ax04,ax05    
    
    def title(axis,year):    
        axis.set_title('year {} '.format(year))
    for n in range(0,4):   
        title(axes_list[n],years[n])# #print (y[n])
        axes_list[n].set_ylim(100,0)
        axes_list[n].set_xlim(6,14)        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[0]):int(y[1])])
        means_getm.append(m)       
               
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)   
                      
    for n in range(0,length,1): #field data
        ax00.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')             
    for m in range(0,int(y[1]),1): #1990
        ax00.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')  


    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[1]):int(y[2])])
        means_getm.append(m)     
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)             
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)       
    for n in range(0,length,1): #field data        
        ax01.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')       
    for m in range(int(y[1]),int(y[2]),1): #1991
        ax01.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[2]):int(y[3])])
        means_getm.append(m)     
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)                  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)              
    for n in range(0,length,1): #field data
        ax02.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')            
    for m in range(int(y[2]),int(y[3]),1): #1992
        ax02.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')     
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[3]):int(y[4])])
        means_getm.append(m)     
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)     
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)          
    for n in range(0,length,1): #field data
        ax03.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')            
    for m in range(int(y[3]),int(y[4]),1): #1993
        ax03.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        


    pdf.savefig()
    #plt.savefig('1980_sal-getm1.png')
    plt.close()   
    
    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    figure.suptitle('Salinity', fontsize=16)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    
    ax00 = figure.add_subplot(gs[0]) # water 
    
    ax01 = figure.add_subplot(gs[1], sharex=ax00) # water 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) # water 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) # water       
    axes_list = (ax00,ax01,ax02,ax03) #,ax04,ax05    
       
    for n in range(0,4):   
        title(axes_list[n],years[n+4])# #print (y[n])
        axes_list[n].set_ylim(100,0)
        axes_list[n].set_xlim(6,14)
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[4]):int(y[5])])
        means_getm.append(m)                      
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
               
    for n in range(0,length,1): #field data
        ax00.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[4]),int(y[5]),1): #1990
        ax00.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')


    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[5]):int(y[6])])
        means_getm.append(m)                      
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
          
    for n in range(0,length,1): #field data
        ax01.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[5]),int(y[6]),1):
        ax01.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[6]):int(y[7])])
        means_getm.append(m)                      
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
    for n in range(0,length,1): #field data
        ax02.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')          
    for m in range(int(y[6]),int(y[7]),1):
        ax02.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[7]):int(y[8])])
        means_getm.append(m)                      
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)   
            
    for n in range(0,length,1): #field data
        ax03.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[7]),int(y[8]),1): 
        ax03.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')    
    

    
    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    #plt.savefig('1980_sal-getm2.png')
    plt.close()  
    
    
    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    figure.suptitle('Salinity', fontsize=16)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    
    ax00 = figure.add_subplot(gs[0]) # water 
    ax00.set_xlim(6,14)
    ax01 = figure.add_subplot(gs[1], sharex=ax00) # water 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) # water 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) # water       
    axes_list = (ax00,ax01,ax02,ax03) #,ax04,ax05    
       
    for n in range(0,4):   
        title(axes_list[n],years[n+8])# #print (y[n])
        axes_list[n].set_ylim(100,0)
        axes_list[n].set_xlim(6,14)
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[8]):int(y[9])])
        means_getm.append(m)                      
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
        
    for n in range(0,length,1): #field data
        ax00.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[8]),int(y[9]),1): #1990
        ax00.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[9]):int(y[10])])
        means_getm.append(m)                      
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
    
            
    for n in range(0,length,1): #field data
        ax01.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')          
    for m in range(int(y[9]),int(y[10]),1):
        ax01.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[10]):int(y[11])])
        means_getm.append(m)                      
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
                
    for n in range(0,length,1): #field data
        ax02.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[10]),int(y[11]),1):
        ax02.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[11]):int(y[12])])
        means_getm.append(m)                      
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
    
            
    for n in range(0,length,1): #field data
        ax03.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[11]),int(y[12]),1): 
        ax03.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')    
    

    
    pdf.savefig() 
    # or you can pass a Figure object to pdf.savefig
    #plt.savefig('1980_sal-getm3.png')
    plt.close()     
    
    
    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    figure.suptitle('Salinity', fontsize=16)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    
    ax00 = figure.add_subplot(gs[0]) # water 
    ax00.set_xlim(6,14)
    ax01 = figure.add_subplot(gs[1], sharex=ax00) # water 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) # water 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) # water       
    axes_list = (ax00,ax01,ax02,ax03) #,ax04,ax05    
       
    for n in range(0,4):   
        title(axes_list[n],years[n+12])# #print (y[n])
        axes_list[n].set_ylim(100,0)
        axes_list[n].set_xlim(6,14)
        means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[12]):int(y[13])])
        means_getm.append(m)                      
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
        
    for n in range(0,length,1): #field data
        ax00.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[12]),int(y[13]),1): #1990
        ax00.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')  
        
        means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[13]):int(y[14])])
        means_getm.append(m)                      
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)    
        
    for n in range(0,length,1): #field data
        ax01.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[13]),int(y[14]),1):
        ax01.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[14]):int(y[15])])
        means_getm.append(m)                      
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
         
    for n in range(0,length,1): #field data
        ax02.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[14]),int(y[15]),1):
        ax02.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807') 
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[15]):int(y[16])])
        means_getm.append(m)                      
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)
            
    for n in range(0,length,1): #field data
        ax03.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[15]),int(y[16]),1): 
        ax03.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')    
    

    
    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    #plt.savefig('1980_sal-getm4.png')
    plt.close()     


    figure = plt.figure(figsize=(11.69, 8.27), dpi=100)
    figure.suptitle('Salinity', fontsize=16)
    gs = gridspec.GridSpec(2,2)
    gs.update(hspace = 0.5)
    
    ax00 = figure.add_subplot(gs[0]) # water 

    ax01 = figure.add_subplot(gs[1], sharex=ax00) # water 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) # water 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) # water       
    axes_list = (ax00,ax01,ax02,ax03) #,ax04,ax05    
       
    for n in range(0,4):   
        title(axes_list[n],years[n+16])# #print (y[n])
        axes_list[n].set_ylim(100,0)
        axes_list[n].set_xlim(6,14)
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[16]):int(y[17])])
        means_getm.append(m)                      
    ax00.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax00.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
    for n in range(0,length,1): #field data
        ax00.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')         
    for m in range(int(y[16]),int(y[17]),1): #1990
        ax00.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[17]):int(y[18])])
        means_getm.append(m)                      
    ax01.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax01.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
    for n in range(0,length,1): #field data
        ax01.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')           
    for m in range(int(y[17]),int(y[18]),1):
        ax01.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[18]):int(y[19])])
        means_getm.append(m)                      
    ax02.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax02.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
        
    for n in range(0,length,1): #field data
        ax02.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')          
    for m in range(int(y[18]),int(y[19]),1):
        ax02.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')
        
        
    means_getm = []
    for n in range(0,len(sal_getm_t)):
        m = np.nanmean(sal_getm_t[n][int(y[19]):int(y[20])])
        means_getm.append(m)                      
    ax03.plot(means_getm,depth_getm,zorder = 10,
          marker = 'o', color = '#d4c42d', markersize = 1)  
    ax03.plot(means,ynew,zorder = 10,
          marker = 'o', color = 'k', markersize = 4)        
        
    for n in range(0,length,1): #field data
        ax03.plot(sal[n],depth[n],linewidth = 0.2,color ='#7dadbc')          
    for m in range(int(y[19]),int(y[20]),1): 
        ax03.plot(sal_getm[m],depth_getm,linewidth = 0.2,color = '#820807')      
    
    pdf.savefig()  # or you can pass a Figure object to pdf.savefig
    #plt.savefig('1980_sal-getm5.png')
    plt.close()          
  
        