'''
Created on 7. feb. 2017

@author: ELP
'''

# script creates two histograms
# with time distribution of data
# reading 2 netcdf files from WOD 


# submodule for reading variables in netcdf format
from netCDF4 import Dataset
#submodule to transfer time from "days after some date" to 
# year and time format 
from netCDF4 import num2date
#module for plotting
import matplotlib.pyplot as plt
# to draw a figure on plot 
import matplotlib.patches as mpatches

# use predefined matplotlib style
plt.style.use('ggplot')

# define the names of netcdf files we want to read
ncfile = 'data_from_OSD_small domain.nc'
ncfile1 = 'data_from_Baltic_small_domain_1980.nc'

# open the file file
fh = Dataset(ncfile, mode='r')
# read needed variable
date_time = fh.variables['date_time'][:]    
# close the file
fh.close()

fh1 = Dataset(ncfile1, mode='r')
date_time1 = fh.variables['date_time'][:]    
fh1.close()

#change the dates units 
dates1 = num2date(date_time1[:],units='days since 1980-01-01',
             calendar='proleptic_gregorian' )

dates = num2date(date_time[:],units='days since 1954-01-01',
             calendar='proleptic_gregorian' )

#create the tuple form dates 
# to have a tuple if a form [year][month][day][hour][minute]...
i = 0  
time = [] 
for n in dates:
    t = n.timetuple()
    time.append(t) #create tuple to select date by month
    i=i+1

i = 0  
time1 = [] 
for n in dates1:
    t = n.timetuple()
    time1.append(t) #create tuple to select date by month
    i=i+1

# create arrays containing only years and months              
years, years1 = [],[]
months, months1 = [],[]
lentime = len(time)     
lentime1 = len(time1) 

for n in range(0,lentime):
    years.append(time[n][0])
    months.append(time[n][1])
        
for n in range(0,lentime1):
    years1.append(time1[n][0])
    months1.append(time1[n][1])    

# define the number of columns in histogram    
num_bins = (max(years)-min(years))
num_bins1 = (max(years1)-min(years1))

# create figure with 2 supblots
fig, (ax, ax2) = plt.subplots(1, 2)

# add histogram
n, bins, patches = ax.hist(years, num_bins,
                histtype='bar',color='#6fc1cc', edgecolor='#4d3514', normed = 1)

n, bins, patches = ax2.hist(years1, num_bins1,
                histtype='bar',color='#6fc1cc', edgecolor='#4d3514', normed = 1)

# add an ellipse
ax.add_patch(mpatches.Ellipse(xy=(1995,0.023), width = 43, height = 0.045,
            linewidth = 1.5, alpha = 1,edgecolor = '#993299', fill = False))

ax.set_title(' a) All available field data')
ax2.set_title('b) Field data since 1980')

# to add months histogram
#num_bins_m = 12
#n, bins, patches = ax3.hist(months1, num_bins_m,
#                histtype='bar',color='#993299', edgecolor='#4d3514',normed = 1)
#ax3.set_title('Months')
#x = [1, 2, 3, 4,5,6,7,8,9,10,11,12,13]
#ax3.set_xticks(x)   

plt.show()
