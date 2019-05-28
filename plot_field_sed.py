'''
Created on 17. mar. 2017

@author: ELP
'''
from netCDF4 import Dataset
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy.ma as ma



plt.style.use('ggplot')




import pandas as pd
import os
import matplotlib.pyplot as plt

path = r'E:\Users\ELP\Python plot\co2marine\input_data'
file =  os.path.join(path,'StBar-2012-3 for Elizaveta.xls')




'''
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

    #def alkdic():
    difs = []
    for n in range(0,len(alk)):
        dif = float(alk[n]) - float(dic[n])
        #difs.append(dif)
        print (dif,alk[n],dic[n])
        
    s3mask = np.isfinite(dic) 
    #print (len(depth))
        #xs = np.arange(0,1)
    s1mask = np.isfinite(dic[0:6])
    s2mask = np.isfinite(dic[6:12])
    s3mask = np.isfinite(dic) 
'''    
    
def print_all(axis,var,title):
    for m in range(1,9):
        axis.plot(var[start_list[m]:end_list[m]],depth[start_list[m]:end_list[m]],
                   linewidth = 0.4, linestyle =  '-', marker='o',
                    markersize= 4)  
        axis.annotate('{}'.format(st_list[m]),(var[end_list[m]-1],
                                                depth[end_list[m]-1]), 
                       arrowprops=dict(arrowstyle="-",ec="k"), #,ec="k" color of line
                       textcoords='offset points',xytext=(-15, -25))  
        axis.set_ylim(18,0)
        axis.set_title('{}'.format(title))

            
#var_list = [h2s,po4,nh4,alk,dic,so4] 
title_list = ['h2s','po4','nh4','alk','dic','so4']  
 
#ax_list = [ax00,ax01,ax02,ax03,ax04,ax05] 
start_list = [0,6,12,18,24,30,36,43,49,55]
end_list = [6,12,18,24,30,36,43,49,55,61]
st_list = [1,6,9,10,11,15,17,19,20,22]



#print (so4)    
plt.show()
#pdf.savefig(figure1)
plt.close()




# create figure with size close to a4 (vertical)
figure = plt.figure(figsize=(8, 9 ), dpi=100)
gs = gridspec.GridSpec(3, 2#,
                   #width_ratios=[1,1],
                   #height_ratios=[1,1]
                   )
gs.update(wspace=0.2,hspace = 0.3,left=0.1,
   right=0.97,bottom = 0.05, top = 0.95) 

ax00 = figure.add_subplot(gs[0])
ax01 = figure.add_subplot(gs[1])    
ax02 = figure.add_subplot(gs[2])
ax03 = figure.add_subplot(gs[3]) 
ax04 = figure.add_subplot(gs[4])
ax05 = figure.add_subplot(gs[5]) 


print_all(ax00,alk , r'$\rm Alkalinity\ \mu M/l$' )
print_all(ax02,h2s,r'$\rm H _2 S\ \mu M/l$')  
print_all(ax03,nh4,r'$\rm NH _4\ \mu M/l$')  
print_all(ax04,po4,r'$\rm PO _4\ \mu M/l$')  
print_all(ax05,so4,r'$\rm SO _4\ \mu M/l$') 

for m in range(1,9):  
    # Dic should bi plotted separately because of NaNs   
    #ax01.plot(dic[start_list[m]:end_list[m]][s3mask[start_list[m]:end_list[m]]],
    #depth[start_list[m]:end_list[m]][s3mask[start_list[m]:end_list[m]]],
    #linewidth = 0.4, linestyle =  '-', marker='o',
    #               markersize= 4)      
    ax01.set_ylim(18,0)
    ax01.set_title('DIC')
    #ax01.annotate('{}'.format(st_list[m]),(dic[end_list[m]-1],
    #                                           depth[end_list[m]-1]), 
    #                  arrowprops=dict(arrowstyle="-",ec="k"),
    
                      #textcoords='offset points',xytext=(-15, -25))          
     
 #for axis in (ax00,ax01,ax02,ax03)  :
 #    axis.set_ylim(20,0)

#for m in range(0,10):
    # start = n        
    # end = n+6
    # ax04.plot(dic[start:end], depth[start:end],'o-')  
    # n = n + 6  






plt.show()

plt.close()
    
    