## CO2 marine
###b3_map.py
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
