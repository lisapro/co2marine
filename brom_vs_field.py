import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
from netCDF4 import Dataset
import numpy as np
import os

plt.style.use('ggplot')

path = r'E:\Users\ELP\Python plot\co2marine\input_data'
fname = (
    r'E:\Users\ELP\Fortran\baltic_2\data_baltic\BROM_Baltic_out.nc') 
fname = (
    r'E:\Users\ELP\Fortran\pom_merge\data\BROM_Baltic_out.nc')  
nc_odv = os.path.join(
    path,'data_from_Baltic_small_domain_1980.nc')
field_file =  os.path.join(
    path,'StBar-2012-3 for Elizaveta.xls')






### Read BROM output  data   
fh =  Dataset(fname)
depth_brom = fh.variables['z'][:] 
depth2_brom = fh.variables['z2'][:] #middle points

kz =  fh.variables['Kz'][:,:]
alk_brom =  fh.variables['Alk'][:,:,:]
dic_brom =  fh.variables['DIC'][:,:]
pH_brom =  fh.variables['pH'][:,:]
po4_brom =  fh.variables['PO4'][:,:]
o2_brom =  fh.variables['O2'][:,:]
no3_brom =  fh.variables['NO3'][:,:]
si_brom =  fh.variables['Si'][:,:]
nh4_brom =  fh.variables['NH4'][:,:]
h2s_brom =  fh.variables['H2S'][:,:]
so4_brom =  fh.variables['SO4'][:,:]
time_brom =  fh.variables['time'][:]

fh.close()

for n in range(0,(len(depth2_brom)-1)):
    if kz[1,n] == 0:
        y2max = depth2_brom[n]         
        ny2max = n         
        break  
    
sed_depth_brom = (depth_brom - y2max) * 100  



### Read porewater data from excel file 
df = pd.read_excel(field_file,'data_geochemistry')
df2 = pd.read_excel(field_file,'data_overlying-bottom water')  

o2 = df2['O2'][1:].astype('float')*1000/32
pH = df2['pH'][1:].astype('float')
depth2 = df2['Distance above sediments'][1:].astype('float')*(-1)

po4 = df['PO43-'][7:]
nh4 = df['NH4+'][7:]
h2s = df['H2S'][7:]
dic = df['DIC'][7:]*1000/12.
alk = df['alkalinity'][7:]*1000 
so4  = df['SO42-'][7:]*1000/(32+(16*4))  
sed_dep = df['Sediment depth'][7:]
wat_dep = (sed_dep - y2max) * 100 

### read ODV water column  netcdf 
fh = Dataset(nc_odv, mode='r')
depthmasked = fh.variables['var1'][:][:]
depth_odv = depthmasked.filled(fill_value= np.nan)    
depth2_odv  = fh.variables['var1'][:][:]    
temp_odv  = fh.variables['var2'][:][:]
sal_odv  = fh.variables['var3'][:][:]    
o2_odv  = fh.variables['var4'][:][:]*44.1
po4_odv  = fh.variables['var5'][:][:]    
si_odv  = fh.variables['var6'][:][:]
no3_odv  = fh.variables['var7'][:][:]        
no2_odv  = fh.variables['var8'][:][:]
pH_odv  = fh.variables['var9'][:][:] 
chl_odv  = fh.variables['var10'][:][:]   
alk_odv  = fh.variables['var12'][:][:]*1000  
date_time_odv = fh.variables['date_time'][:]    
lat_odv  = fh.variables['latitude'][:]
long_odv  = fh.variables['longitude'][:]                            
fh.close()
  
  
 

#line colors
summ = '#d0576f'  #'#d75752' #
wint =  '#8dc0e7' #'#d75752' 
spr_aut ='#998970'  #'#d75752' #

def make_figure():
    figure = plt.figure(figsize=(6, 8 ))
    gs = gridspec.GridSpec(2, 2)
    gs.update(wspace=0.2,hspace = 0.2,left=0.15,
       right=0.97,bottom = 0.05, top = 0.9) 
    
    ax00 = figure.add_subplot(gs[0])
    ax01 = figure.add_subplot(gs[1])    
    ax02 = figure.add_subplot(gs[2])
    ax03 = figure.add_subplot(gs[3]) 
    
    return ax00,ax01,ax02,ax03  
  
def make_figure1():
    figure = plt.figure(figsize=(6, 8))
    gs = gridspec.GridSpec(1, 1)
    gs.update(wspace=0.2,hspace = 0.2,left=0.15,
       right=0.97,bottom = 0.05, top = 0.9) 
    
    ax00 = figure.add_subplot(gs[0])    
    return ax00   


def plot_comparison(d_min,d_max,y,x1,x2,x3,x4,pl_sed = False,
                    pl_water = False):
    f = {'so4': (so4_brom,so4),'dic':(dic_brom,dic),
         'h2s': (h2s_brom,h2s),'nh4':(nh4_brom,nh4),
         'o2': (o2_brom,o2)}
    
    a = 0.5
    l = 0.5
    ax00.set_title(x1)  
    ax01.set_title(x2)  
    ax02.set_title(x3)  
    ax03.set_title(x4)
    
    for n in range(365,3650,30):    
        if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter" 
            c = wint
        elif n >= 150 and n < 249: #"summer"  
            c = summ
        else : #"autumn and spring"
            c = spr_aut
                  
        ax00.plot(f[x1][0][n][d_min:d_max,0],
                  y[d_min:d_max],alpha = a,
                  linewidth = l,
                  zorder = 1, c = c)        
                                
        ax01.plot(f[x2][0][n][d_min:d_max,0],
                  y[d_min:d_max],alpha = a, 
                  linewidth = l,zorder = 1,
                  c = c) 
                    
        ax02.plot(f[x3][0][n][d_min:d_max,0],
                  y[d_min:d_max],alpha = a, 
                  linewidth = l,zorder = 1, c = c) 
        ax03.plot(f[x4][0][n][d_min:d_max,0],
                  y[d_min:d_max],alpha = a, 
                  linewidth = l ,zorder = 1, c = c) 
        
        if pl_sed == True: 
            if x1 == 'o2':
                sed_dep = depth2    
            ax00.plot(f[x1][1],sed_dep,
                      'ko--',linewidth = l,zorder = 10)       
            ax01.scatter(f[x2][1],sed_dep, c = 'k',zorder = 10)          
            ax02.plot(f[x3][1],sed_dep,
                      'ko--',linewidth = l,zorder = 10)  
            ax03.plot(f[x4][1],sed_dep,
                      'ko--',linewidth = l,zorder = 10)
            
        elif pl_water == True: 
            pass         
                            
#def pl2(var1,var2,var3,var4):
#    functions = {'so4': 'SO42-',
def plot_comparison1(d_min,d_max,y,sed_dep,x1,pl_sed = False,
                    pl_water = False):
    f = {'so4': (so4_brom,so4,None),'dic':(dic_brom,dic,None),
         'h2s': (h2s_brom,h2s,None),'nh4':(nh4_brom,nh4,None),
         'o2': (o2_brom,o2,o2_odv),
         'si':(si_brom,None,si_odv),
         'no3':(no3_brom,None,no3_odv),'pH':(pH_brom,pH,pH_odv),
         'alk':(alk_brom,alk,alk_odv),
         'po4':(po4_brom,po4,po4_odv)}

    a = 0.5
    l = 0.5
    ax00.set_title(x1)  
    
    for n in range(0,365,10):    
        if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter" 
            c = wint
        elif n >= 150 and n < 249: #"summer"  
            c = summ
        else : #"autumn and spring"
            c = spr_aut
        
          
        ax00.plot(f[x1][0][n][d_min:d_max,0],
                  y[d_min:d_max],alpha = a,
                  linewidth = l,
                  zorder = 10, c = c)        
        
        if pl_sed == True: 
            dep = sed_dep
            if x1 == 'o2':
                dep = depth2  
            if x1 in ('o2','dic'):                   
                ax00.scatter(f[x1][1],sed_dep,
                      c = 'k',zorder = 10)       
            else:     
                ax00.plot(f[x1][1],sed_dep,
                      'ko--',linewidth = l,zorder = 10)  
                          
        elif pl_water == True:


            if x1 in ('o2','pH'):
                dep = (depth2/100 + y2max) 
            else:    
                dep = (sed_dep/100 + y2max)
            #print (len(dep),len(f[x1][1]))          
            if (f[x1][1] is None) is False:
                #print ('in',len(f[x1][1]),len(dep),len(sed_dep))
                ax00.scatter(f[x1][1],dep,alpha= a,
                          c = 'k',zorder = 10)
            
            if (f[x1][2] is None) is False:
                ax00.scatter(f[x1][2],depth_odv,alpha= a,
                        c = 'y',zorder = 5)
 
                               
def plot_sediment(x1,x2,x3,x4):
    #plt.clf()
    #
    for axis in (ax00,ax01,ax02,ax03):
        axis.set_ylim(18,-5)
        axis.axhspan(0,18,color='#b08b52',
                    alpha = 0.4,label = "sediment"  )
        axis.axhspan(-3,0,color='#dbf0fd',
                    alpha = 0.7,label = "water" ) 

    d_min_sed = 75 #80
    d_max_sed = None
    plot_comparison(d_min_sed,d_max_sed,sed_depth_brom,sed_dep,
                  x1,x2,x3,x4,True)
    #plt.savefig(
    #    'results/comparison_sed_{}_{}_{}_{}.png'.format(
    #        x1,x2,x3,x4))
    plt.show()
    #plt.close()

        
def plot_water(x1,x2,x3,x4):
    #plt.clf()

    d_min_wat = 0
    d_max_wat = 80
    for axis in (ax00,ax01,ax02,ax03):
        axis.set_ylim(80,0)
        axis.axhspan(0,80,color='#dbf0fd',
                    alpha = 0.7,label = "water" )    
    plot_comparison(d_min_wat,d_max_wat,depth_brom,
                  x1,x2,x3,x4,False,True)
    plt.savefig(
        'results/comparison_wat_{}_{}_{}_{}.png'.format(
            x1,x2,x3,x4))  
    plt.clf()  
    #plt.show()
    
def plot_sediment1(x1):
    ax00.set_ylim(18,-5)
    ax00.axhspan(0,18,color='#b08b52',
                    alpha = 0.4,label = "sediment"  )
    ax00.axhspan(-5,0,color='#dbf0fd',
                    alpha = 0.7,label = "water" ) 

    d_min_sed = 75 #80
    d_max_sed = None
    plot_comparison1(d_min_sed,d_max_sed,sed_depth_brom,
                     sed_dep, x1,True,False)
    #plt.savefig(
    #    'results/comparison_sed_{}_{}_{}_{}.png'.format(
    #        x1,x2,x3,x4))
    #plt.show()
    #plt.close()
        
def plot_water1(x1):
    #plt.clf()

    d_min_wat = 0
    d_max_wat = 80
    #for axis in (ax00,ax01,ax02,ax03):
    ax00.set_ylim(80,0)
    ax00.axhspan(0,80,color='#dbf0fd',
                    alpha = 0.7,label = "water" )    
    plot_comparison1(d_min_wat,d_max_wat,depth_brom,
                     sed_dep,x1,False,True)
    #plt.savefig(
    #    'results/comparison_wat_{}_{}_{}_{}.png'.format(
    #        x1))  
    #plt.clf()  
    #plt.show()




#print (functions['so4'][1])
#plot_sediment(so4_brom,dic_brom,h2s_brom,nh4_brom)

#figure 1, uncomment to show
#ax00,ax01,ax02,ax03 = make_figure()
#plot_sediment('so4','dic','h2s','nh4')

#figure 2
#ax00,ax01,ax02,ax03 = make_figure()
#plot_water('so4','dic','h2s','nh4')

#pl_2('so4','dic','h2s','nh4')
#plot_water(alk_brom)
    

'''
#ax00,ax01,ax02,ax03 = make_figure()
for var in ('o2','dic','so4','h2s','nh4','po4'):
    ax00 = make_figure1()
    plot_sediment1(var)
    #plt.savefig('results/comparison_sed_{}.png'.format(var))  
    plt.show()
''' 
for var in ('dic','so4','pH',
            'po4','si','no3','alk','o2'):
    ax00 = make_figure1()
    plot_water1(var)
    plt.savefig('results/comparison_wat_{}.png'.format(var))  
    #plt.show() 
       



 


