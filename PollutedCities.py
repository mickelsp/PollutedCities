## Create Graphs and a Map of Most Polluted Cities of World
import numpy as np
import xlrd as excel
import geopy as gp
import re as re
import pickle
#gn = gp.geocoders.Nominatim()
gn = gp.geocoders.GeoNames(username='mickelsp')

## Define Functions
def isFloat(string): # This one tells me whether a string is a float or something else.
    try:
        float(string)
        return True
    except ValueError:
        return False

## Import Data from Excel File
fileDirectory = "/Users/mickelsp/Documents/Polluted Cities/"
fileName = "PollutedCitiesDatabase.xls"

pollutionData = excel.open_workbook(fileDirectory+fileName)
cityLevelData = excel.Book.sheet_by_name(pollutionData,"cities")

# Extract data from individual cell
# excel.book.sheet.Sheet.cell(cityLevelData,row,column)

# Extract data by column or row
#excel.book.sheet.Sheet.col(cityLevelData,rowNumber)
#excel.book.sheet.Sheet.row(cityLevelData,colNumber)

# Extract city names and pollution levels
countryListRaw = excel.book.sheet.Sheet.col(cityLevelData,2)
cityListRaw = excel.book.sheet.Sheet.col(cityLevelData,3)
pm10ListRaw = excel.book.sheet.Sheet.col(cityLevelData,4)      # [micrograms/cubic meter] Particulate matter between 2.5 and 10 microns
pm25ListRaw = excel.book.sheet.Sheet.col(cityLevelData,7)      # [micrograms/cubic meter] Particulate matter smaller than 2.5 microns

# City and country lists need cleaning up because each cell contains "text: " before the name (that's because it's a cell type), as well as eliminating some parentheticals    
cityList = []; countryList = []; pm10List = []; pm25List = [];  # Initialize vectors
counter = 0
startIndex = 2; stopIndex = 1623;   # Indices of first and last cities. Stuff before and after isn't data
for city in cityListRaw[startIndex:stopIndex]:
    cityName = re.sub('\(\w*\)', '',cityListRaw[counter].value)
    countryName = re.sub('\(\w*\)', '',countryListRaw[counter].value)
    if isFloat(pm10ListRaw[counter].value):     # Convert string to float
        pm10 = pm10ListRaw[counter].value
    else:
        pm10 = 0                                # If string is empty, then make it zero
    if isFloat(pm25ListRaw[counter].value):     # Convert string to float
        pm25 = pm25ListRaw[counter].value
    else:
        pm25 = 0                                # If string is empty, then make it zero
                
    cityList.append(cityName)                   # Create a list of all city names
    countryList.append(countryName)             # Create a list of all country names
    pm10List.append(pm10)                       # Create a list of all pm10 values
    pm25List.append(pm25)                       # Create a list of all pm25 values
    counter = counter + 1

# Sort lists by key value (i.e. by pm10 or pm 25 values) to place highest polluting cities at top of list
citiesByPM10 = [(cityList,countryList,pm10List) for (pm10List, cityList, countryList) in sorted(zip(pm10List,cityList,countryList),reverse=True)]
citiesByPM25 = [(cityList,countryList,pm25List) for (pm25List, cityList, countryList) in sorted(zip(pm25List,cityList,countryList),reverse=True)]

# Look up latitude and longitude of cities we're interested in
mapThisList = []; skipped = []; counter = 0;    # Initialize lists
for city in citiesByPM10[0:49]:                 # Only look at top 30 cities for now
    cityName = citiesByPM10[counter][0]
    countryName = citiesByPM10[counter][1]
    latlong = gn.geocode(cityName+", "+countryName)
    if latlong:
        mapThisList.append((cityName,countryName,latlong[1][0],latlong[1][1],citiesByPM10[counter][2]))     # Create a list of cities for which we successfully find lat/long coordinates
    else: 
        skipped.append((cityName,countryName,citiesByPM10[counter][2]))                                     # Note for which cities we did not find lat/long coordinates
    counter = counter + 1
    
# Save data for the cities we want to look at to a file to open in another script
outputFileName = 'top50pm10cities.txt'
with open(fileDirectory+outputFileName, 'wb') as fo:
    pickle.dump(mapThisList, fo)
fo.close()    # Close opened file

mapThisList2 = []; skipped2 = []; counter = 0;    # Initialize lists
for city in citiesByPM25[0:49]:                 # Only look at top 30 cities for now
    cityName = citiesByPM25[counter][0]
    countryName = citiesByPM25[counter][1]
    latlong = gn.geocode(cityName+", "+countryName)
    if latlong:
        mapThisList2.append((cityName,countryName,latlong[1][0],latlong[1][1],citiesByPM25[counter][2]))     # Create a list of cities for which we successfully find lat/long coordinates
    else: 
        skipped2.append((cityName,countryName,citiesByPM25[counter][2]))                                     # Note for which cities we did not find lat/long coordinates
    counter = counter + 1

# Save data for the cities we want to look at to a file to open in another script
outputFileName = 'top50pm25cities.txt'
with open(fileDirectory+outputFileName, 'wb') as fo:
    pickle.dump(mapThisList2, fo)
fo.close()    # Close opened file