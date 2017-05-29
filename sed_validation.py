'''
Created on 20. feb. 2017

@author: ELP
'''

from  matplotlib.backends.backend_pdf import PdfPages
from netCDF4 import Dataset
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy.ma as ma
import os,sys
from tkinter.filedialog import askopenfilename
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import  QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets

plt.style.use('ggplot')

#plt.style.use('ggplot')
#read input file 
with open('field1.txt', 'r') as f:
    # important to specify delimiter right 
    reader = csv.reader(f, delimiter='\t')
    r = []
    for row in reader:
        # if you don't know which delimiter is used 
        # print one row to view it 
        #print (row)
        #break
        r.append(row)        
    r1 = np.transpose(np.array(r[2:]) ) # skip two header lines
    depth = r1[1]

    h2s = r1[2]
    so4 = r1[3]
    nh4 = r1[4]
    po4 = r1[5]
    alk = r1[6]
    dic = np.array(r1[7]).astype(np.double)
    #dic_masked = np.ma.masked_where(dic == 'NaN' , dic)
    #dicmask = np.isfinite(dic_masked)
    #print (dic_masked)
ask_filename = askopenfilename(initialdir= os.getcwd(),
                           filetypes =(("NetCDF file", "*.nc"),("All Files","*.*")),
                           title = "Choose a file.")
#fname = 'BROM_Baltic_out_b3_15_1998_10cm.nc'    
fname = os.path.split(ask_filename)[1] # 'BROM_Baltic_out_0604171year.nc'    
print (fname)
fh =  Dataset(fname)
depth_brom = fh.variables['z'][:] 
depth2_brom = fh.variables['z2'][:] #middle points
kz =  fh.variables['Kz'][:,:]
alk_brom =  fh.variables['Alk'][:,:,:]
dic_brom =  fh.variables['DIC'][:,:]
po4_brom =  fh.variables['PO4'][:,:]
nh4_brom =  fh.variables['NH4'][:,:]
h2s_brom =  fh.variables['H2S'][:,:]
so4_brom =  fh.variables['SO4'][:,:]
time_brom =  fh.variables['time'][:]


for n in range(0,(len(depth2_brom)-1)):
    if kz[1,n] == 0:
        y2max = depth2_brom[n]         
        ny2max = n         
        break  


to_float = []
for item in depth_brom:
    to_float.append(float(item)) #make a list of floats from tuple 
depth_sed = [] # list for storing final depth data for sediment 
v=0  
for i in to_float:
    v = (i- y2max)*100  #convert depth from m to cm
    depth_sed.append(v)
sed_depth_brom = depth_sed   
        
fh.close()

with PdfPages('sed_val_{}.pdf'.format(fname)) as pdf: 
           
    s3mask = np.isfinite(dic) 
    #print (len(depth))
        #xs = np.arange(0,1)
    s1mask = np.isfinite(dic[0:6])
    s2mask = np.isfinite(dic[6:12])
    s3mask = np.isfinite(dic) 
    def print_all(axis,var,title):
        #n = 0  
        for m in range(1,9):
            #start = n        
            #end = n+6
            axis.plot(var[start_list[m]:end_list[m]],depth[start_list[m]:end_list[m]],
                      linewidth = 0.4, linestyle =  '-', marker='o',
                       markersize= 4)  
            axis.annotate('{}'.format(st_list[m]),(var[end_list[m]-1],
                                                   depth[end_list[m]-1]), 
                          arrowprops=dict(arrowstyle="-"),
                          textcoords='offset points',xytext=(-15, -25))  
            axis.set_ylim(18,0)
            axis.set_title('{}'.format(title))

               
    var_list = [h2s,po4,nh4,alk,dic,so4] 
    title_list = ['h2s','po4','nh4','alk','dic','so4']  
     
    #ax_list = [ax00,ax01,ax02,ax03,ax04,ax05] 
    start_list = [0,6,12,18,24,30,36,43,49,55]
    end_list = [6,12,18,24,30,36,43,49,55,61]
    st_list = [1,6,9,10,11,15,17,19,20,22]
    #for n in range(0,len(var_list)):      
    #    print_all(ax_list[n],var_list[n])        
    #    ax_list[n].set_title(title_list[n])
    #    ax_list[n].set_ylim(17,0)
    #print_all(ax01,po4)
 
    
    # create figure with size close to a4 (vertical)
    figure1 = plt.figure(figsize=(10, 8 ), dpi=100)
    gs = gridspec.GridSpec(2, 2,
                       width_ratios=[1,1],
                       height_ratios=[1,1]
                       )
    gs.update(wspace=0.2,hspace = 0.2,left=0.1,
       right=0.97,bottom = 0.05, top = 0.9) 

    ax00 = figure1.add_subplot(gs[0]) # map
    ax01 = figure1.add_subplot(gs[1]) 
    ax03 = figure1.add_subplot(gs[3]) # so4      
    # Here we can add some text
    ax01.axis('off')  # Create plot but dont show it
    
    
    ax02 = figure1.add_subplot(gs[2]) # po4
    # po4 from brom
    #print(len(time_brom))
    
    #line colors
    summ = '#d0576f' 
    wint =  '#8dc0e7'
    spr_aut ='#998970'
                                  
    #ax02.plot(po4_brom[0],sed_depth_brom)            

    
    for n in range(0,365):
        if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter" 
            ax02.plot(po4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = wint) 
            ax03.plot(so4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = wint)              
        elif n >= 150 and n < 249: #"summer"
            ax02.plot(po4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = summ )  
            ax03.plot(so4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = summ )                          
        else : #"autumn and spring"
            ax02.plot(po4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1,c = spr_aut) 
            ax03.plot(so4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1,c = spr_aut )           
                    
    ax01.text(0, 0.90, "Input T,S,Kz from GETM - 1993 year"  
                    "\nField data - March 2012 year \nThird line") #x,y

    # coordinated of field data with 
    # biogeochemical data  from Polish institute 
    lat_bgch = [55.5372,55.51843333,55.50116667,
                55.52833333,55.5397, 55.50871667,
                55.51025,55.48216667,55.45198333,
                55.54351667]
    
    lon_bgch = [18.27465, 18.20873333, 18.23761667,
                18.20283333,18.25776667, 18.2381,18.25151667,
                18.17466667,18.17215, 18.26866667]
    
    st_bgch =  [20,22, 11,1,6,9,10,15,17,19]
    
    ax00.set_title('Stations')
    ax00.scatter(lon_bgch, lat_bgch, zorder = 6,
                label='hydrological, geochemical, biological sampling',
                 s = 10)
    
    # coordinated of TS input from GETM model
    b3_getm = [18.1555,55.4863] # E,N 
    
    ax00.scatter(b3_getm[0],b3_getm[1], label='model T,S, input data ',
            s = 100, zorder = 5)
    ax00.annotate('GETM\ninput',(b3_getm[0],b3_getm[1]),
                xytext=(15, 5), ha='right', va='bottom',
                textcoords='offset points', zorder = 10)
    for i, txt in enumerate(st_bgch):
        ax00.annotate(txt, (lon_bgch[i],lat_bgch[i]),xytext=(17, 0),
                ha='right', va='bottom',textcoords='offset points'  )
        
    print_all(ax02,po4,r'$PO _4$')  
    print_all(ax03,so4,r'$SO _4$') 
    #print (so4)    
    #plt.show()
    plt.savefig('sed_val1.png')
    pdf.savefig(figure1)
    plt.close()




    # create figure with size close to a4 (vertical)
    figure2 = plt.figure(figsize=(10, 8 ), dpi=100)
    gs = gridspec.GridSpec(2, 2,
                       width_ratios=[1,1],
                       height_ratios=[1,1]
                       )
    gs.update(wspace=0.2,hspace = 0.2,left=0.1,
       right=0.97,bottom = 0.05, top = 0.9) 

    ax00 = figure2.add_subplot(gs[0])
    ax01 = figure2.add_subplot(gs[1])    
    ax02 = figure2.add_subplot(gs[2])
    ax03 = figure2.add_subplot(gs[3]) 
    #ax04 = figure.add_subplot(gs[4])
    #ax05 = figure.add_subplot(gs[5]) 
    
    
    print_all(ax00,alk,'Alkalinity')      
    print_all(ax02,h2s,'H2S')  
    print_all(ax03,nh4,'NH4')  
    
    for m in range(1,9):  
        # Dic should bi plotted separately because of NaNs   
        ax01.plot(dic[start_list[m]:end_list[m]][s3mask[start_list[m]:end_list[m]]],
        depth[start_list[m]:end_list[m]][s3mask[start_list[m]:end_list[m]]],
        linewidth = 0.4, linestyle =  '-', marker='o',
                       markersize= 4)      
        ax01.set_ylim(18,0)
        ax01.set_title('DIC')
        ax01.annotate('{}'.format(st_list[m]),(dic[end_list[m]-1],
                                                   depth[end_list[m]-1]), 
                          arrowprops=dict(arrowstyle="-"),
                          textcoords='offset points',xytext=(-15, -25))          
    for n in range(0,365):
        if n >= 0 and n<=60 or n >= 335 and n <365 : #"winter" 
            
            ax00.plot(alk_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = wint)                 
            ax01.plot(dic_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = wint)             
            ax02.plot(h2s_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = wint) 
            ax03.plot(nh4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = wint)              
        elif n >= 150 and n < 249: #"summer"
            ax00.plot(alk_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = summ )            
            ax01.plot(dic_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = summ )            
            ax02.plot(h2s_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = summ )  
            ax03.plot(nh4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1, c = summ )                          
        else : #"autumn and spring"
            ax00.plot(alk_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1,c = spr_aut)             
            ax01.plot(dic_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1,c = spr_aut)             
            ax02.plot(h2s_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1,c = spr_aut) 
            ax03.plot(nh4_brom[n],sed_depth_brom,alpha = 0.1, 
                      linewidth = 0.1 , zorder = 1,c = spr_aut )          
            #n = n + 6  '''        
    #for axis in (ax00,ax01,ax02,ax03)  :
    #    axis.set_ylim(20,0)

    '''#for m in range(0,10):
       # start = n        
       # end = n+6
       # ax04.plot(dic[start:end], depth[start:end],'o-')  
       # n = n + 6  
    ''' 

    #plt.show()
    plt.savefig('sed_val2.png')    
    pdf.savefig(figure2)

    plt.close()

















    
    
    