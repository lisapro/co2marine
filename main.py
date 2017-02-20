'''
Created on 2. feb. 2017

@author: ELP
'''
# Script makes plots for BROM output comparing 
#with WOD data
# Creates separated pdf(or png) files and can
# combine them into 1 multipage pdf

import pdb #python debugger 
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
plt.style.use('ggplot')

def read_netcdf_odv(ncfile):

    fh = Dataset(ncfile, mode='r')

    #depth = fh.variables['var1'][:][:]
    depthmasked = fh.variables['var1'][:][:]
    depth = depthmasked.filled(fill_value= np.nan)    
    depth2 = fh.variables['var1'][:][:]
    
    temp = fh.variables['var2'][:][:]
    sal = fh.variables['var3'][:][:]    
    o2 = fh.variables['var4'][:][:]
    po4 = fh.variables['var5'][:][:]    
    si = fh.variables['var6'][:][:]
    no3 = fh.variables['var7'][:][:]        
    no2 = fh.variables['var8'][:][:]
    pH = fh.variables['var9'][:][:] 
    chl = fh.variables['var10'][:][:]   
    alk = fh.variables['var12'][:][:]   
    date_time = fh.variables['date_time'][:]    
    lat = fh.variables['latitude'][:]
    long = fh.variables['longitude'][:]
                                 
    fh.close()

    dates = num2date(date_time[:],units='days since 1990-01-01',
                 calendar='proleptic_gregorian' )
    
    return depth,temp,sal,o2,po4,si,no3,no2,pH,chl,dates,alk,depth2

ncfile = 'data_from_OSD_small domain.nc'
w = read_netcdf_odv(ncfile)

depth = w[0]
temp = w[1] 
sal = w[2]
o2 = w[3]
po4 = w[4]
si = w[5]
no3 = w[6]
no2 = w[7]
pH = w[8]
chl = w[9]
dates = w[10]
alk = w[11]
depth2 = w[12] 

#o2[o2 > 0] =  o2 * 46.6
o2_2 = o2 * 46.6 # change units from ml/l to mmol/l
pH_2 = pH - 0.11 # conversion from NBS scale to Total

#def read_necdf_brom(ncfile_brom):


#fh1 = Dataset('BROM_Baltic_outnewsulfates.nc', mode='r')
#fh1 = Dataset('BROM_Baltic_out_so4_6000.nc', mode='r')
#fh1 = Dataset('BROM_Baltic_outnewsulfates.nc', mode='r')
#fh1 = Dataset('BROM_Baltic_out_time_changed_2005.nc', mode='r')
#nc_file_brom = 'BROM_Baltic_out_1992.nc'
nc_file_brom = 'BROM_Baltic_out_1993.nc'


fh1 = Dataset(nc_file_brom, mode='r')

depth_brom = fh1.variables['z'][:]    
depth2_brom =  fh1.variables['z2'][:] #middle points
kz =  fh1.variables['Kz'][:,:]
o2_brom  =  fh1.variables['O2'][:,:]
sal_brom  =  fh1.variables['S'][:,:]
temp_brom = fh1.variables['T'][:,:]
pH_brom = fh1.variables['pH'][:,:]
po4_brom = fh1.variables['PO4'][:,:]
no2_brom = fh1.variables['NO2'][:,:]
no3_brom = fh1.variables['NO3'][:,:]
si_brom = fh1.variables['Si'][:,:]
alk_brom = fh1.variables['Alk'][:,:]

fh1.close()  



len_depth2_brom = depth2_brom.size 
       
for n in range(0,(len_depth2_brom-1)):
    if kz[1,n] == 0:
        y2max = depth2[n]         
        ny2max = n         
        break
                 
def figure_pdf(var_wod,var_brom,varname):
    with PdfPages('Baltic_validation_{}.pdf'.format(varname)) as pdf:

        # As many times as you like, create a figure fig and save it:
        figure = plt.figure(figsize=( 11.69 ,8.27), dpi=100)
        gs = gridspec.GridSpec(2,2)
        gs.update(wspace=0.1,hspace = 0.2,left=0.04,
               right=0.99,bottom = 0.04, top = 0.9) 
        ax00 = figure.add_subplot(gs[0])     
        ax01 = figure.add_subplot(gs[1])      
        ax02 = figure.add_subplot(gs[2])  
        ax03 = figure.add_subplot(gs[3])         
        ax00.set_title('{} from BROM all days'.format(varname))  
        ax01.set_title('{} from BROM every 10 day'.format(varname))
        ax02.set_title('{} from WOD '.format(varname))
        ax03.set_title('BROM vs WOD ')       
        #plt.plot(range(7), [3, 1, 4, 1, 5, 9, 2], 'r-o')
        plt.title('{} from BROM all days'.format(varname))
        ax00.set_ylim(100,0)
        ax01.set_ylim(100,0)
        ax02.set_ylim(100,0)
        ax03.set_ylim(100,0)
        #if str(var_brom) == str(o2_brom) :
        #    ax00.set_xlim(0,550)
            
        for ax in (ax00,ax01,ax02,ax03):
            if str(var_brom) == str(o2_brom) :
                ax.set_xlim(-0.5,550)
            elif str(var_brom) == str(sal_brom) :   
                ax.set_xlim(6,15)
            elif str(var_brom) == str(temp_brom) :   
                ax.set_xlim(-0.5,24)                
            elif str(var_brom)== str(pH_brom) :   
                ax.set_xlim(6.5,9.5)   
            elif str(var_brom) == str(po4_brom) :   
                ax.set_xlim(-0.5,5)
            elif str(var_brom) == str(si_brom) :   
                ax.set_xlim(-0.5,80)                                               
            elif str(var_brom) == str(no3_brom) :   
                ax.set_xlim(-0.5,12)                
            else: 
                pass  
        for m in range(0,365,1):
            ax00.plot(var_brom[m][0:ny2max],depth_brom[0:ny2max],
                      linewidth = 0.2,color = 'red') #n - day 
        
        lenght = (len(var_wod))                 
        for n in range(0,lenght): #field data
            ax03.plot(var_wod[n],depth[n],linewidth = 0.2, color = '#7dadbc')
            ax02.plot(var_wod[n],depth[n],linewidth = 0.5) 
            
        for m in range(0,365,10):
            ax01.plot(var_brom[m][0:ny2max],depth_brom[0:ny2max],
                      linewidth = 0.2, color = 'red') #n - day
            ax03.plot(var_brom[m][0:ny2max],depth_brom[0:ny2max],
                      linewidth = 0.4, color = '#b62733',) #n - day   
            
        ax03.plot(var_wod[0],depth[0],linewidth = 0.2, color = '#7dadbc',
                      alpha = 1, label= u"field")#, alpha= 0.5
        ax03.plot(var_brom[0][0:ny2max],depth_brom[0:ny2max],linewidth = 0.4,
                      color = '#b62733',label= u"modelled") #n - day   
        legend = ax03.legend( shadow=False, loc='best') #bbox_to_anchor=(0.8, 0.35))  
        frame = legend.get_frame()
        frame.set_facecolor('white')             
                       
        #pdf.savefig(fig)
        # When no figure is specified the current figure is saved 
             
        #plt.show()         
        pdf.savefig()
        plt.savefig('Baltic_validation_{}.png'.format(varname))
        plt.close()  
       
                 
        d = pdf.infodict()
        d['Title'] = 'Multipage PDF Example'
        d['Author'] = u'Elizaveta Protsenko\xe4nen'
        d['Subject'] = 'BROM model validation'
        #d['Keywords'] = 'PdfPages multipage keywords author title subject'
        #d['CreationDate'] = datetime.datetime(2009, 11, 13)
        d['ModDate'] = datetime.datetime.today()  


def show_figure(var_wod,var_brom,varname):
    #print (depth2[0])
    figure = plt.figure(figsize = (10,6))
    gs = gridspec.GridSpec(2,2)
    gs.update(wspace=0.3,hspace = 0.4,left=0.04,
               right=0.99,bottom = 0.04, top = 0.9) 
    ax00 = figure.add_subplot(gs[0]) # water     
    ax01 = figure.add_subplot(gs[1]) # water       
    ax02 = figure.add_subplot(gs[2]) # water   
    ax03 = figure.add_subplot(gs[3]) 
    
    #len = ma.shape(o2)#(len(o2))
    lenght = (len(var_wod))
    

    #len_depth2 = len(depth2_brom)
    #def calculate_ybbl():
    for n in range(0,(len_depth2_brom-1)):
        if kz[1,n] == 0:
            y2max = depth2[n]         
            ny2max = n         
            break
    
            
    #ax00.set_title('Var from BROM all days')
    #plt.title('{}month{}_{}.txt'.format(boundary,month,name)) 
    ax00.set_title('{} from BROM all days'.format(varname))  
    ax01.set_title('{} from BROM every 10 day'.format(varname))
    ax02.set_title('{} from WOD '.format(varname))
    ax03.set_title('BROM vs WOD ')
    ax00.set_ylim(100,0)
    ax01.set_ylim(100,0)
    ax02.set_ylim(100,0)
    ax03.set_ylim(100,0)
    
    for m in range(0,365,1):
        ax00.plot(var_brom[m][0:ny2max],depth_brom[0:ny2max],
                  linewidth = 0.2,color = 'red') #n - day  
        
    #print(len(depth_roms))
    for n in range(0,lenght,1): #field data
        ax03.plot(var_wod[n],depth[n],linewidth = 0.2, color = '#7dadbc')
        ax02.plot(var_wod[n],depth[n],linewidth = 0.5) 
        
    for m in range(0,365,10):
        ax01.plot(var_brom[m][0:ny2max],depth_brom[0:ny2max],
                  linewidth = 0.2, color = 'red') #n - day
        ax03.plot(var_brom[m][0:ny2max],depth_brom[0:ny2max],
                  linewidth = 0.4, color = '#b62733',) #n - day   
        
    #legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax03.plot(var_wod[0],depth[0],linewidth = 0.2, color = '#7dadbc',
                  alpha = 1, label= u"field")#, alpha= 0.5
    ax03.plot(var_brom[0][0:ny2max],depth_brom[0:ny2max],linewidth = 0.4,
                  color = '#b62733',label= u"modelled") #n - day   
    legend = ax03.legend( shadow=False,bbox_to_anchor=(0.8, 0.35))  
    frame = legend.get_frame()
    frame.set_facecolor('white')          
    plt.show() 
 
    
filenames = []
def files(varname):
    #varnames.append(varname)
    filenames.append('Baltic_validation_{}.pdf'.format(varname))    

def write_pdf():    

    figure_pdf(o2_2,o2_brom,'O2')
    files('O2')
    figure_pdf(sal,sal_brom,'Salinity')
    files('Salinity')
    figure_pdf(temp,temp_brom,'Temperature')
    files('Temperature')
    figure_pdf(pH_2,pH_brom,'pH') #Change the scale!! 
    files('pH')
    figure_pdf(po4,po4_brom,'PO4')
    files('PO4')
    figure_pdf(si,si_brom,'Si')
    files('Si')
    figure_pdf(no3,no3_brom,'NO3')
    files('NO3')
    
    merger = PdfFileMerger()
    for filename in filenames:
        merger.append(filename)    
    ####    merger.append(PdfFileReader(file(filename, 'rb')))
    merger.write("merged_Baltic_validation_{}.pdf".format(nc_file_brom))
    



write_pdf() 

#show_figure(pH_2,pH_brom,'pH') 
#show_figure(temp,temp_brom,'Temp') 


def print_kz():
    figure = plt.figure(figsize = (10,6))
    gs = gridspec.GridSpec(1,1)
    gs.update(wspace=0.3,hspace = 0.4) 
    ax00 = figure.add_subplot(gs[0]) # water     
    ax00.set_ylim(100,0)
    for m in range(0,365,1): 
        ax00.plot(kz[m], depth2_brom,
                  linewidth = 0.2,color = 'red')       
    plt.show()

    
if __name__ == '__main__':
    pass