'''
Created on 16. mar. 2017

@author: ELP
'''
import csv
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

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
 
# create first figure    
figure = plt.figure(figsize=( 11,8 ), dpi=100)                
gs = gridspec.GridSpec(3,1)
gs.update(hspace = 0.3,left=0.05,
       right=1,bottom = 0.05, top = 0.95) 

ax00 = figure.add_subplot(gs[0])   
ax00.set_title(r'$\rm Alkalinity\ \mu M/l$')  
alk_plot = ax00.scatter(day,depth,s = 9, c = alk, edgecolor='#59544a',
                        linewidth= 0.2, cmap='jet')
cbar = plt.colorbar(alk_plot)

ax01 = figure.add_subplot(gs[1])  
ax01.set_title("pH NBS") 
pH_plot = ax01.scatter(day,depth,s = 9, c = pH, edgecolor='#59544a',
                linewidth= 0.2, cmap='jet',zorder = 10, vmin=7, vmax=9)
cbar = plt.colorbar(pH_plot)

ax02 = figure.add_subplot(gs[2])   
ax02.set_title(r"$\rm Si\ \mu M/l$")  
si_plot = ax02.scatter(day,depth,s = 9, c = si, edgecolor='#59544a',
                        linewidth= 0.2, cmap='jet')
cbar = plt.colorbar(si_plot)

for ax in (ax00,ax01,ax02) :
    ax.set_ylim(95,0) 
    ax.set_xlim(0,365)

figure.savefig('Relax_files_alkphsi.png') 
# to make background of figure transparent - , transparent=True
#plt.show()

# open second set of files 
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

figure2 = plt.figure(figsize=( 11,8 ), dpi=100) 
              
gs2 = gridspec.GridSpec(3,1)
gs2.update(hspace = 0.3,left=0.05,
       right=1,bottom = 0.05, top = 0.95)

ax02 = figure2.add_subplot(gs2[0])   
ax02.set_title(r"$\rm PO_4\ \mu M/l$")  
po4_plot = ax02.scatter(day,depth,s = 9, c = po4, edgecolor='#59544a',
                linewidth= 0.2, cmap='jet')
cbar = plt.colorbar(po4_plot)

ax03 = figure2.add_subplot(gs2[1])
ax03.set_title(r"$\rm O_2\ \mu M/l$")
o2_plot = ax03.scatter(day,depth,s = 9, c=o2, edgecolor='#59544a',
                       linewidth= 0.2, cmap='jet')
cbar = plt.colorbar(o2_plot)

ax04 = figure2.add_subplot(gs2[2])  
ax04.set_title(r"$\rm NO_3\ \mu M/l$")
no3_plot = ax04.scatter(day,depth,s = 9, c = no3, edgecolor='#59544a',
                        linewidth= 0.2, cmap='jet')
cbar = plt.colorbar(no3_plot)

for ax in (ax02,ax03,ax04) :
    ax.set_ylim(95,0) 
    ax.set_xlim(0,365)

figure2.savefig('Relax_files_po4o2no3.png') 
#plt.show()

'''with open('chlorophyll_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    po4 = np.array(r1[2]) '''
f.close() 
