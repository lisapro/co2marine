'''
Created on 7. feb. 2017

@author: ELP
'''
# Script reads Netcdf file with GETM output and WOD data for chosen region 
# It Plots vertical profiles of Temperature for each day from GETM 
# And vertical profiles of Temperature for each station at WOD
# Each subplot contains data from one year

# It calculates and plots the year average profiles for GETM and WOD data 
# calculates and prints the total difference ( by abs values) 
# between GETM and WOD averages 

from netCDF4 import Dataset
from netCDF4 import num2date, date2num
from datetime import datetime, timedelta,date
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_pdf import PdfPages

plt.style.use('ggplot')

#ncfile = 'data_from_OSD_small domain.nc'
ncfile = 'data_from_Baltic_small_domain_1980.nc'
from scipy import interpolate
# to draw a figure on plot 
import matplotlib.patches as mpatches

fh = Dataset(ncfile, mode='r')
date_time = fh.variables['date_time'][:]
tempmasked = fh.variables['var2'][:][:]
temp = tempmasked.filled(fill_value= np.nan) 
depthmasked = fh.variables['var1'][:][:]
depth = depthmasked.filled(fill_value= np.nan)   
    
fh.close()

dates = num2date(date_time[:],units='days since 1980-01-01',
             calendar='proleptic_gregorian' )


#read netcdf with getm_data
fh2 = Dataset('B3zax-kz.nc')
dd = np.array(fh2.variables['zax'][:])   
depth_getm = dd * -1
tt = np.ravel(fh2.variables['temp'][:])    
temp_getm = np.reshape(tt,(7670,78))
temp_getm_t = temp_getm.transpose()

    
dates_2 = [datetime(1990,1,1)+n*
         timedelta(days=365) for n in range(22)]  
y = date2num(dates_2, units = 'days since 1990-01-01',
                 calendar= 'proleptic_gregorian')

i = 0  
time = [] 
for n in dates:
    i=i+1
    t = n.timetuple()
    time.append(t) #create tuple to select dat by month
    #return time
    
# create empty arrays to store separately
#data from different years
    
depths_1990, depths_1991,depths_1992 = [],[],[]
depths_1993,depths_1994, depths_1995 = [],[],[]
depths_1996,depths_1997, depths_1998 = [],[],[]
depths_1999,depths_2000, depths_2001 = [],[],[]
depths_2002,depths_2003, depths_2004 = [],[],[]
depths_2005,depths_2006, depths_2007 = [],[],[]
depths_2008,depths_2009 = [],[]

temps_1990, temps_1991,temps_1992 = [],[],[]
temps_1993,temps_1994,temps_1995 = [],[],[]
temps_1996,temps_1997, temps_1998 = [],[],[]
temps_1999,temps_2000, temps_2001 = [],[],[]
temps_2002,temps_2003, temps_2004 = [],[],[]
temps_2005,temps_2006, temps_2007 = [],[],[]
temps_2008,temps_2009 = [],[]

j=0  
for n in time:
    if n[0] == 1990: #n[1] - place of month in a time tuple                
        depths_1990.append(depth[j])
        temps_1990.append(temp[j])    
        j =j +1
    elif n[0] == 1991: #n[1] - place of month in a time tuple                
        depths_1991.append(depth[j])
        temps_1991.append(temp[j])        
        j =j +1      
    elif n[0] == 1992: #n[1] - place of month in a time tuple                
        depths_1992.append(depth[j])
        temps_1992.append(temp[j])        
        j =j +1   
    elif n[0] == 1993: #n[1] - place of month in a time tuple                
        depths_1993.append(depth[j])
        temps_1993.append(temp[j])        
        j =j +1   
    elif n[0] == 1994: #n[1] - place of month in a time tuple                
        depths_1994.append(depth[j])
        temps_1994.append(temp[j])        
        j =j +1   
    elif n[0] == 1995: #n[1] - place of month in a time tuple                
        depths_1995.append(depth[j])
        temps_1995.append(temp[j])        
        j =j +1       
    elif n[0] == 1996: #n[1] - place of month in a time tuple                
        depths_1996.append(depth[j])
        temps_1996.append(temp[j])        
        j =j +1          
    elif n[0] == 1997: #n[1] - place of month in a time tuple                
        depths_1997.append(depth[j])
        temps_1997.append(temp[j])        
        j =j +1          
    elif n[0] == 1998: #n[1] - place of month in a time tuple                
        depths_1998.append(depth[j])
        temps_1998.append(temp[j])        
        j =j +1          
    elif n[0] == 1999: #n[1] - place of month in a time tuple                
        depths_1999.append(depth[j])
        temps_1999.append(temp[j])        
        j =j +1          
    elif n[0] == 2000: #n[1] - place of month in a time tuple                
        depths_2000.append(depth[j])
        temps_2000.append(temp[j])        
        j =j +1          
    elif n[0] == 2001: #n[1] - place of month in a time tuple                
        depths_2001.append(depth[j])
        temps_2001.append(temp[j])        
        j =j +1          
    elif n[0] == 2002: #n[1] - place of month in a time tuple                
        depths_2002.append(depth[j])
        temps_2002.append(temp[j])        
        j =j +1         
    elif n[0] == 2003: #n[1] - place of month in a time tuple                
        depths_2003.append(depth[j])
        temps_2003.append(temp[j])        
        j =j +1         
    elif n[0] == 2004: #n[1] - place of month in a time tuple                
        depths_2004.append(depth[j])
        temps_2004.append(temp[j])        
        j =j +1         
    elif n[0] == 2005: #n[1] - place of month in a time tuple                
        depths_2005.append(depth[j])
        temps_2005.append(temp[j])        
        j =j +1         
    elif n[0] == 2006: #n[1] - place of month in a time tuple                
        depths_2006.append(depth[j])
        temps_2006.append(temp[j])        
        j =j +1 
    elif n[0] == 2007: #n[1] - place of month in a time tuple                
        depths_2007.append(depth[j])
        temps_2007.append(temp[j])        
        j =j +1 
    elif n[0] == 2008: #n[1] - place of month in a time tuple                
        depths_2008.append(depth[j])
        temps_2008.append(temp[j])        
        j =j +1 
    elif n[0] == 2009: #n[1] - place of month in a time tuple                
        depths_2009.append(depth[j])
        temps_2009.append(temp[j])        
        j =j +1                         
                                              
    else: 
        j =j +1      
           
 
     
years = ['1990','1991','1992','1993','1994','1995','1996','1997',
         '1998','1999','2000','2001','2002','2003','2004','2005',
         '2006','2007','2008','2009','2010']

depth_y_list = [depths_1990, depths_1991,depths_1992,
                depths_1993,depths_1994, depths_1995,
                depths_1996,depths_1997, depths_1998,
                depths_1999,depths_2000, depths_2001,
                depths_2002,depths_2003, depths_2004,
                depths_2005,depths_2006, depths_2007,
                depths_2008,depths_2009]


temp_y_list = [temps_1990, temps_1991,temps_1992,
               temps_1993,temps_1994,temps_1995,
               temps_1996,temps_1997, temps_1998,
               temps_1999,temps_2000, temps_2001,
               temps_2002,temps_2003, temps_2004,
               temps_2005,temps_2006, temps_2007,
               temps_2008,temps_2009]


m = len(temp) 
col = '#6fc1cc' # #9f2439' #color 
fd_col = '#d5c6b0'
l = 0.5 # linewidth


# Here we interpolate temperature to standard levels 
temp_int = []
for n in range(0,m): # take all stations, m = len(temp)
    f = interpolate.interp1d(depth[n],temp[n],bounds_error=False, fill_value=np.nan)
    ynew = np.arange(0,100, 5) #define the grid of st. levels 
    xnew = f(ynew)   # use interpolation function returned by `interp1d`
    temp_int.append(xnew)


# here we calculate the mean value for all st. levels 
means = []    
temp_int_t = (np.array(temp_int)).T #transpose array 
len_temp_int = len(temp_int_t)


for n in range(0,len_temp_int): #take all values at one level 
    mean_temp = np.nanmean(temp_int_t[n]) # calc mean avoiding nan values
    means.append(mean_temp)  

with PdfPages('def_typical_year_T.pdf') as pdf:
    #figure = plt.figure(figsize = (14,7)) #figsize=(8.27, 11.69), dpi=100
    figure = plt.figure(figsize=(8.27, 11.69), dpi=100)
    figure.suptitle('Temperature from WOD, different years', fontsize=16)
    
    
    gs = gridspec.GridSpec(6,2)
    
    ax00 = figure.add_subplot(gs[0]) 
    ax01 = figure.add_subplot(gs[1], sharex=ax00) 
    ax02 = figure.add_subplot(gs[2], sharex=ax00) 
    ax03 = figure.add_subplot(gs[3], sharex=ax00) 
    ax04 = figure.add_subplot(gs[4]) 
    ax05 = figure.add_subplot(gs[5], sharex=ax00) 
    ax06 = figure.add_subplot(gs[6], sharex=ax00) 
    ax07 = figure.add_subplot(gs[7], sharex=ax00) 
    ax08 = figure.add_subplot(gs[8], sharex=ax00) 
    ax09 = figure.add_subplot(gs[9], sharex=ax00) 
    ax10 = figure.add_subplot(gs[10], sharex=ax00) 
    ax11 = figure.add_subplot(gs[11], sharex=ax00) 
    
    figure1 = plt.figure(figsize=(8.25, 11.68), dpi=100)
    figure1.suptitle('Temperature from WOD, different years', fontsize=16)
    gs1 = gridspec.GridSpec(6,2)
    gs.update(left=0.05, right=0.99, bottom = 0.04, top = 0.94,wspace=0.2,hspace = 0.4)
    gs1.update(left=0.05, right=0.99, bottom = 0.04, top = 0.94,wspace=0.2,hspace = 0.4)
    ax00_1 = figure1.add_subplot(gs1[0]) 
    ax01_1 = figure1.add_subplot(gs1[1], sharex=ax00_1) 
    ax02_1 = figure1.add_subplot(gs1[2], sharex=ax00_1) 
    ax03_1 = figure1.add_subplot(gs1[3], sharex=ax00_1) 
    ax04_1 = figure1.add_subplot(gs1[4]) 
    ax05_1 = figure1.add_subplot(gs1[5], sharex=ax00_1) 
    ax06_1 = figure1.add_subplot(gs1[6], sharex=ax00_1) 
    ax07_1 = figure1.add_subplot(gs1[7], sharex=ax00_1) 
    
    
    axes_list = (ax00,ax01,ax02,ax03,ax04,ax05,ax06,ax07,ax08,ax09,
                    ax10,ax11,ax00_1,ax01_1,ax02_1,ax03_1,ax04_1,ax05_1,ax06_1,ax07_1) 

 
    
    def plot_all_years_mean(axis,zorder):#all years mean
        axis.plot(means,ynew,zorder = zorder,
              marker = 'o', color = 'k',
               #color = '#ffb200',markeredgecolor = '#d18b00', 
               markersize = 4)  
    
    
    def plot_year_mean(axis,temp_year, depth_year,zorder):
        
        i = len(temp_year) 
        temp_y_int = []
        year_means = []    
        
        for n in range(0,i):
            f = interpolate.interp1d(depth_year[n],temp_year[n],
                                     bounds_error=False,
                                      fill_value=np.nan)
            ynew = np.arange(0,100, 5) #define the grid of st. levels 
            xnew = f(ynew)   # use interpolation function returned by `interp1d`
            temp_y_int.append(xnew)        
    
        temp_y_int_t = (np.array(temp_y_int)).T #transpose array 
        len_temp_y_int = len(temp_y_int_t) 
        j = 0
        difs = []
        
        for n in range(0,len_temp_y_int): #take all values at one level 
            mean_y_temp = np.nanmean(temp_y_int_t[n]) # calc mean avoiding nan values
            dif_mean = mean_y_temp - means[j]
            year_means.append(mean_y_temp)
            difs.append(abs(dif_mean))
            j += 1 
            
        sum_difs = np.nansum(difs)         
        #print (round(sum_difs)) 
           
    
        axis.text(11, 79, 'total diff = {}'.format(round(sum_difs)), fontsize=13)
        axis.plot(year_means,ynew,zorder = zorder,
              marker = 'o', color = '#993299', markersize = 3)  
        
        #axis.plot(difs,ynew,zorder = zorder,
        #      marker = 'o', color = 'r', markersize = 3)     
    
    def plot_all_fielddata(axis,zorder):       
        for n in np.arange(0,m,1): #field data        
            axis.plot(temp[n],depth[n],linewidth = l,
                  color = fd_col,alpha = 0.5,zorder = zorder) #blue    
    
       
    def plot_yearly_fielddata(axis,temp_arr,depth_arr,zorder):
        m = len(temp_arr)    
        for n in range(0,m,1): #field data    # yellow      
            axis.plot(temp_arr[n],depth_arr[n], # move it to the front layer
                      linewidth = l,color = col,zorder = zorder )
     
                          
    def plot_yearly_getm(axis,t_start,t_stop,zorder):
        for m in range(int(t_start),int(t_stop),1): #1990 Getm data                   red
            axis.plot(temp_getm[m],depth_getm,linewidth = 0.2,color = '#820807',
                      zorder = zorder)       
    

    s = len(axes_list)
            
    for n in np.arange(0,s):
        plot_all_fielddata(axes_list[n],1)        
        plot_yearly_fielddata(axes_list[n],temp_y_list[n],depth_y_list[n],2) 
         
        plot_all_years_mean(axes_list[n],4)
        plot_year_mean(axes_list[n], temp_y_list[n],depth_y_list[n],5)  
           
        axes_list[n].set_ylim(100,0)
        axes_list[n].set_title(years[n])   
        
    
    
    ax03.add_patch(mpatches.Ellipse(xy=(16, 75,), width = 12, height = 26,
                linewidth = 1.5, alpha = 1,edgecolor = '#993299', fill = False))
    ax08.add_patch(mpatches.Ellipse(xy=(16, 75,), width = 12, height = 26,
                linewidth = 1.5, alpha = 1,edgecolor = '#993299', fill = False))
      
    # save both figures to multipage pdf 

    # plt.savefig('<filename.png>')
    pdf.savefig(figure) 
    # and in separate png with
    figure.savefig('typical_year1.png') 
    plt.close()
    pdf.savefig(figure1) 
    figure1.savefig('typical_year2.png')      
    plt.close()           
    # to show figures here                  
    #plt.show()
