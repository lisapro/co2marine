'''
Created on 20. apr. 2017

@author: ELP
'''
'''
Created on 16. mar. 2017

@author: ELP
'''
from netCDF4 import Dataset
import csv
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename
plt.style.use('ggplot')
# open dat files for each variable
# detphs and days are the save in every file
# so I read it only one time 
 
with open('alk_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    day = r1[0]
    depth = r1[1]
    alk = np.array(r1[2])
f.close()
with open('pH_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    pH = np.array(r1[2]) 
f.close()

with open('si_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )   
    si = np.array(r1[2]) 
f.close()

with open('po4_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    po4 = np.array(r1[2]) 
f.close() 

with open('o2_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    o2 = np.array(r1[2]) 
f.close()
with open('no3_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    no3 = np.array(r1[2]) 
f.close()

root = tk.Tk()
root.withdraw() 
ask_filename = askopenfilename(initialdir= os.getcwd(),
                filetypes =(("NetCDF file", "*.nc"),
                ("All Files","*.*")),title = "Choose a file.")
fname = ask_filename #os.path.split(ask_filename)[1] 
fh = Dataset(fname)
depth_brom = np.array(fh.variables['z'][:])  
alk_brom =  np.array(fh.variables['Alk'][:])
pH_brom = np.array(fh.variables['pH'][:])
si_brom = np.array(fh.variables['Si'][:])
po4_brom = np.array(fh.variables['PO4'][:])
o2_brom = np.array(fh.variables['O2'][:])
no3_brom = np.array(fh.variables['NO3'][:])

#print (alk_brom[0].shape,depth_brom.shape)
# create first figure    
figure = plt.figure() #figsize=( 11,8 ), dpi=100               
gs = gridspec.GridSpec(2,2)
gs.update(hspace = 0.3,left=0.05,
       right=0.97,bottom = 0.05, top = 0.95) 

ax00 = figure.add_subplot(gs[0])
ax01 = figure.add_subplot(gs[1])   
ax00_1 = figure.add_subplot(gs[2])
ax01_1 = figure.add_subplot(gs[3]) 

figure2 = plt.figure() #figsize=( 11,8 ), dpi=100               

 
ax02 = figure2.add_subplot(gs[0])
ax03 = figure2.add_subplot(gs[1])   
ax04 = figure2.add_subplot(gs[2])  
ax05 = figure2.add_subplot(gs[3])


ax00.set_title(r'$\rm Alkalinity\ \mu M/l$') 
for n in range(0,365,10): 
    ax00.plot(alk_brom[n][0:80],depth_brom[0:80])
    ax00_1.plot(alk_brom[n][80:],depth_brom[80:])
ax00.scatter(alk,depth, s= 0.3) #, ,
                        #linewidth= 0.2, cmap='jet'
ax00.set_ylim(78,0)
ax00_1.set_ylim(78.7,78.4)

 
ax01.set_title("pH NBS") 
for n in range(0,365,10): 
    ax01.plot(pH_brom[n][0:80],depth_brom[0:80])
ax01.scatter(pH,depth, s= 0.3)
#pH_plot = ax01.scatter(day,depth,s = 9, c = pH, edgecolor='#59544a',
#                linewidth= 0.2, cmap='jet',zorder = 10, vmin=7, vmax=9)
#cbar = plt.colorbar(pH_plot)
ax01.set_ylim(78,0)

  
ax02.set_title(r"$\rm Si\ \mu M/l$")  
for n in range(0,365,10): 
    ax02.plot(si_brom[n][0:80],depth_brom[0:80])
ax02.scatter(si,depth, s= 0.3) #
                        #linewidth= 0.2, cmap='jet'
ax02.set_ylim(78,0)

   
ax03.set_title(r"$\rm PO _4\ \mu M/l$")  
for n in range(0,365,10): 
    ax03.plot(po4_brom[n][0:80],depth_brom[0:80])
ax03.scatter(po4,depth, s= 0.3) #
                        #linewidth= 0.2, cmap='jet'
ax03.set_ylim(78,0)

ax04.set_title(r"$\rm O_2\ \mu M/l$")
for n in range(0,365,10): 
    ax04.plot(o2_brom[n][0:80],depth_brom[0:80])
ax04.scatter(o2,depth, s= 0.3) #
                        #linewidth= 0.2, cmap='jet'
ax04.set_ylim(78,0)
 

ax05.set_title(r"$\rm NO_3\ \mu M/l$") 
for n in range(0,365,10): 
    ax05.plot(no3_brom[n][0:80],depth_brom[0:80])
ax05.scatter(no3,depth, s= 0.3) #
                        #linewidth= 0.2, cmap='jet'
ax05.set_ylim(78,0) 
 
    
plt.show()

#figure.savefig('Relax_files_alkphsi.png') 
# to make background of figure transparent - , transparent=True
#plt.show()




'''
figure2.savefig('Relax_files_po4o2no3.png') 
#plt.show()

 '''
