## CO2 marine
Set of scripts using for validating brom to field data 
### b3_map.py
The script creates a map of spatial distrubution for available data from:
WOD (World Ocean Database), field data, modeling input. 
It reads nc file containing WOD data (produced by ODV - Ocean Data View program). 
All other coordinated are hardcoded. 
### def_typical_year.py
The script reads Netcd files with GETM output and WOD data for chosen region, plots vertical profiles of Temperature for each day from GETM and vertical profiles of Temperature for each station at WOD.
Each subplot contains data from one year. Also, tt calculates and plots the year average profiles for GETM and WOD data, 
calculates and prints the total difference ( by abs values) between GETM and WOD averages 
### main.py
This script makes plots for BROM output comparing with WOD dat, creates separated pdf(or png) files and can combine them into 1 multipage pdf
### stat_dates.py
This script creates two histograms with time distribution of data, reading 2 netcdf files from WOD 
### sal_getm.py and temp_getm.py
These scripts read Netcdf file with GETM output and WOD data for chosen region. 
Plot vertical profiles of temperature ( of salinity) for each day from GETM (each subplot containg on year of GETM data) and for each station at WOD (All WOD data at each subplot).
It calculates and plots the year vertical average profiles for GETM and WOD data.  
### create_relax_files.py 
Script creates averaged seasonal profile for Si, NO3, PO4, O2, Alk,and pH from WOD 
1. read variable in a file (name is variable is input argument to function, you call it later) 
2. Cycle to remove stations where all the values are nan    
3. Transpose array
4. Delete columns ( used to be rows before trasnponation) containing only nans ( it does not affect 1d numdays array) 
5. Transpose back
6. Interpolate to standard horizonts ynew = np.arange(0,100, 1)
7. Function to select data by one month. 
8. Transpose and calculate mean for each standard horizont. call function to calculate means for each month
9. Now we have 1d array with mean, st. horizonts for 1 month.
10. write this array n times, n = number of days in this month. 
11. Transpose array, flatten it. 
12. For Alkalinity and Oxygen we convert units to micromoles/l
13. Create 2d array of numbers of days 
14. Plot means to check 
15. Create 2d array with depths,numbers of days, concentrations of variable and save it to txt file 
