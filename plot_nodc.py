'''
Created on 16. mar. 2017

@author: ELP
'''
import csv
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

with open('alk_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    
    #print (r1)
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


   
figure = plt.figure(figsize=( 11,8 ), dpi=100)                
gs = gridspec.GridSpec(2,1)
gs.update(wspace=0.1,hspace = 0.2,left=0.1,
       right=0.99,bottom = 0.2, top = 0.9) 

ax00 = figure.add_subplot(gs[0])   
ax00.set_title("Alkalinity mumol/l")  
#ax00.grid(b=False)

ax00.set_facecolor('#f8f6f1')     


m = ax00.scatter(day,depth,s = 9, c = alk, edgecolor='#59544a', linewidth= 0.2, 
                  cmap='jet',zorder = 10 )
ax00.set_ylim(95,0)
cbar = plt.colorbar(m)#, orientation='horizontal'


ax01 = figure.add_subplot(gs[1])  
ax01.set_ylim(95,0) 
ax01.set_title("pH NBS") 
pH_plot = ax01.scatter(day,depth,s = 9, c = pH, edgecolor='#59544a', linewidth= 0.2, 
                  cmap='jet',zorder = 10, vmin=7, vmax=9)

cbar = plt.colorbar(pH_plot)

ax01.set_ylim(95,0)

figure.savefig('Relax_files_1.png', transparent=True) 
#plt.show()


with open('si_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    day = r1[0]
    depth = r1[1]    
    si = np.array(r1[2]) 
f.close() 

with open('no3_out.dat', 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    r = []
    for row in reader:
        r.append(row)
    r1 =np.transpose(np.array(r[:]) )
    no3 = np.array(r1[2]) 
f.close() 

figure1 = plt.figure(figsize=( 11,8 ), dpi=100)                
gs2 = gridspec.GridSpec(2,1)
gs2.update(wspace=0.1,hspace = 0.2,left=0.1,
       right=0.99,bottom = 0.2, top = 0.9) 

ax02 = figure1.add_subplot(gs2[0])   
ax02.set_title("Si mumol/l")  
#ax00.grid(b=False)

ax02.set_facecolor('#f8f6f1')     

m = ax02.scatter(day,depth,s = 9, c = si, edgecolor='#59544a', linewidth= 0.2, 
                  cmap='jet',zorder = 10 )
ax02.set_ylim(95,0)
cbar = plt.colorbar(m)#, orientation='horizontal'


ax03 = figure1.add_subplot(gs2[1])  
ax03.set_ylim(95,0) 
ax03.set_title("NO3 mumol/l") 
no3_plot = ax03.scatter(day,depth,s = 9, c = no3, edgecolor='#59544a', linewidth= 0.2, 
                  cmap='jet',zorder = 10 )
cbar = plt.colorbar(no3_plot)

ax03.set_ylim(95,0)

#plt.show()
figure1.savefig('Relax_files_2.png', transparent=True) 
plt.close()



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

figure2 = plt.figure(figsize=( 11,8 ), dpi=100) 
               
gs2 = gridspec.GridSpec(2,1)
gs2.update(wspace=0.1,hspace = 0.2,left=0.1,
       right=0.99,bottom = 0.2, top = 0.9) 

ax02 = figure2.add_subplot(gs2[0])   
ax02.set_title("PO4 mumol/l")  
#ax00.grid(b=False)

ax02.set_facecolor('#f8f6f1')     

m = ax02.scatter(day,depth,s = 9, c = po4, edgecolor='#59544a', linewidth= 0.2, 
                  cmap='jet',zorder = 10 )
ax02.set_ylim(95,0)
cbar = plt.colorbar(m)#, orientation='horizontal'

ax03 = figure2.add_subplot(gs2[1])  
ax03.set_ylim(95,0) 
ax03.set_title("O2 ml/l") 
o2_plot = ax03.scatter(day,depth,s = 9, c =o2, edgecolor='#59544a', linewidth= 0.2, 
                  cmap='jet',zorder = 10 )
cbar = plt.colorbar(o2_plot)

ax03.set_ylim(95,0)

figure2.savefig('Relax_files_3.png', transparent=True) 
plt.close()
