'''
Created on 22. feb. 2017

@author: ELP
'''
from operator import itemgetter
from netCDF4 import Dataset,num2date, date2num
import numpy as np
import matplotlib.pyplot as plt 
from scipy import interpolate
from scipy.interpolate import griddata
import matplotlib.gridspec as gridspec
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline
import os 
    
path = r'E:\Users\ELP\Python plot\co2marine\input_data'   
odvfile = os.path.join(path,'data_from_Baltic_small_domain_1980.nc') 

def readfile(ncfile,name_in_file,varname):
    # Read  data from netcdf file 
    fh = Dataset(ncfile, mode='r')
    #1 - read data
    depth_nan = (fh.variables['var1'][:][:]).filled(fill_value= np.nan)
    date_time_nan = fh.variables['date_time'][:]       
    var_nan =  (fh.variables[name_in_file][:][:]).filled(fill_value= np.nan) 
                  
    fh.close()

    dates = num2date(date_time_nan[:],units='days since 1980-01-01',
                 calendar='proleptic_gregorian' )
    
    # to_date_tuple
    months_nan = []
    for n in dates:
        t = n.timetuple()
        months_nan.append(t[1]) 
    
    #2  delete nans by columns
    # cycle to remove stations where all the values are nan    
    var = []
    months = []
    depth = []
    l = len(var_nan)
    for n in range(0,l):
        a = var_nan[n]
        t = months_nan[n]
        d = depth_nan[n]
        if np.isnan(a).all()== True:
            #print ('all is nan') #or np.isnan(z).all()== True: 
            continue
        else :
            var.append(a)   
            months.append(t) 
            depth.append(d)
        pass
    
    #3  transpose array 
    var = np.array(var).T     
    depth = np.array(depth).T    
    months = np.array(months)  
     
    #4  delete columns ( used to be rows before trasnposition)
    #   containing only nans ( it does not affect 1d numdays array) 
    var2 = []
    #date_time2 = []
    depth2 = []
    l = len(var)
    for n in range(0,l):
        a = var[n]
        d = depth[n]
        if np.isnan(a).all()== True:
            continue
        else :
            var2.append(a)   
            depth2.append(d)
        pass
    var2 = np.array(var2)

    
    #5  transpose back 
    var = np.array(var2).T  
    depth = np.array(depth2).T     
    
    #6 interpolate to standard levels
    var_int = []
    ynew = np.arange(0,85, 1)
    length = (len(var))
    for n in range(0,length):
        f = interpolate.interp1d(depth[n],var[n], bounds_error=False,
                                  fill_value='extrapolate',kind = 'linear')#'nearest')
        xnew = f(ynew)   # use interpolation function returned by `interp1d`
        var_int.append(xnew)
     
    var_int = np.array(var_int)   # now the array keeps values on stand. depths
    depth_int = ynew    #new depths  


    #7. select data by one month. 
    def select_by_month(month,var):
        j=0 
        var_m = []     
          
        for n in months:
            if n == month: #n[1] - place of month in a time tuple
                var_m.append(var_int[j])   
                j =j +1
            else: 
                j =j +1     
    
        #8 transpose and calculate mean for each standard horizont.  
        var_m = np.array(var_m)      
        var_m_t = np.array(var_m).T
    
        means = []    
        max = len(var_m_t)
        for n in range(0,max):        
            a = var_m_t[n]   
            m = np.nanmean(a)
            means.append(m)  
        means = np.array(means).T    
            
        return   var_m,means  

    # call function to calculate means for each month
    var_m, mean_m  = select_by_month(1,var_int) #jan[0], jan[1]
    var_m_2, mean_m_2  = select_by_month(2,var_int) # feb[0], feb[1]
    var_m_3, mean_m_3  = select_by_month(3,var_int) #mar[0], mar[1]
    var_m_4, mean_m_4  = select_by_month(4,var_int) #apr[0], apr[1]
    var_m_5, mean_m_5  = select_by_month(5,var_int) #may[0], may[1]
    var_m_6, mean_m_6  = select_by_month(6,var_int) #june[0], june[1]
    var_m_7, mean_m_7  = select_by_month(7,var_int) #july[0], july[1]
    var_m_8, mean_m_8  = select_by_month(8,var_int) #aug[0], aug[1]
    var_m_9, mean_m_9  = select_by_month(9,var_int) #sept[0], sept[1]
    var_m_10, mean_m_10  = select_by_month(10,var_int) #okt[0], okt[1]
    var_m_11, mean_m_11  = select_by_month(11,var_int) #nov[0], nov[1]
    var_m_12, mean_m_12  = select_by_month(12,var_int) #dec[0], dec[1]    
    #return depth_int,months,var_int,varname #depth_nan,var_nan,date_time_nan|


    array1 = []
    depth1 = []
    days = []
    
    #lenghesof months        
    monthes = [31,28,31,30,31,30,31,31,30,31,30,31]
    means = [mean_m,mean_m_2,mean_m_3,mean_m_4,
             mean_m_5,mean_m_6,mean_m_7, mean_m_8,
             mean_m_9,mean_m_10,mean_m_11,mean_m_12]
    
    len_means = len(means)
    
    boundary_top = []
    for n in range(0,12):
        if varname == 'alk':
            i = means[n][0]*1000
            boundary_top.append(i)
        elif varname == 'o2' :
            i = means[n][0]* 44.6 
            boundary_top.append(i) 
        elif varname == 'phytoplankton'  : 
            i = means[n][0]/4.    
            boundary_top.append(i)               
        else :     
            i = means[n][0]
            boundary_top.append(i)

    
    x = np.linspace(1,12,12)
    f = interp1d(x, boundary_top, kind='cubic')
    
    spl = UnivariateSpline(x, boundary_top)
    if varname == "pH":
        spl.set_smoothing_factor(0)
    elif varname == 'no3': 
        spl.set_smoothing_factor(0.1)
    elif varname == 'alk': 
        spl.set_smoothing_factor(20000)

    return spl,varname,x,boundary_top

fig3 = plt.figure(figsize= (5,7))
gs = gridspec.GridSpec(5, 1) 
gs.update(left=0.1, right=0.97,top = 0.91,bottom = 0.07,
                   wspace=0.2,hspace=0.3) 
ax = fig3.add_subplot(gs[0])
ax1 = fig3.add_subplot(gs[1])

ax2 = fig3.add_subplot(gs[2])
ax3 = fig3.add_subplot(gs[3])
ax4 = fig3.add_subplot(gs[4])

for axis in (ax1,ax2,ax3,ax):
    axis.tick_params(bottom='off',labelbottom='off')    
xnew = np.linspace(1, 12, num=365, endpoint=True)

def plot(axis,varodv,varname):
    datafile = readfile(odvfile,varodv,varname)
    #ax 
    spl = datafile[0]
    varname = datafile[1]
    x = datafile[2]
    boundary_top = datafile[3]
    axis.set_title('{}_top boundary condition'.format(varname))
    axis.scatter(x, boundary_top,c ='k')
    axis.plot(xnew, spl(xnew), 'k', lw=1)
    np.savetxt('{}_top_boundary.dat'.format(varname), boundary_top,delimiter=' ')
    
plot(ax,'var12','alk')
plot(ax1,'var7','no3')
plot(ax2,'var6','si')
plot(ax3,'var5','po4')
plot(ax4,'var4','o2')

#fig3.savefig('top_boundary_conditions.png')
plt.show()
plt.close()   


#data = readfile('data_from_Baltic_small_domain_1980.nc','var10','chlorophyll')
#data = readfile('data_from_Baltic_small_domain_1980.nc','var10','phytoplankton')
#data = readfile('data_from_Baltic_small_domain_1980.nc','var9','pH')   
#combined_top = np.vstack((xnew,spl(xnew))) #.T #days,
#np.savetxt('{}_top_boundary.dat'.format(varname), (spl(xnew)), delimiter=' ')  

