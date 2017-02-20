## CO2 marine
###b3_map.py
The script creates a map of available data. form WOD, field data, modeling input 
### def_typical_year.py
The script reads Netcd files with GETM output and WOD data for chosen region, plots vertical profiles of Temperature for each day from GETM and vertical profiles of Temperature for each station at WOD.
Each subplot contains data from one year. Also, tt calculates and plots the year average profiles for GETM and WOD data, 
calculates and prints the total difference ( by abs values) between GETM and WOD averages 
### main.py
This script makes plots for BROM output comparing with WOD dat, creates separated pdf(or png) files and can combine them into 1 multipage pdf


