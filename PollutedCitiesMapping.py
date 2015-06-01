## Plot Polluted Cities on Map
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib.cm as cm
import numpy as np
import pickle

## Import Data from Saved File
fileDirectory = "/Users/mickelsp/Documents/Polluted Cities/"
fileName = 'top50pm10cities.txt'
#fileName = 'top50pm25cities.txt'

with open(fileDirectory+fileName, 'rb') as fo:
    mapThisList = pickle.load(fo)
    
## Form lat/long data
lats = np.arange(0.0,len(mapThisList),1.0); lons = np.arange(0.0,len(mapThisList),1.0); pm10 = np.arange(0.0,len(mapThisList),1.0);
counter = 0
for item in mapThisList:
    lats[counter] = float(mapThisList[counter][2])
    lons[counter] = float(mapThisList[counter][3])
    pm10[counter] = float(mapThisList[counter][4])
    counter = counter + 1

scalefactor = 100
pm10 = scalefactor * np.pi*(pm10/max(pm10))**2               # Scale to get a usable area

## Actually form map
# Convert latitude and longitude into the Mercator projection
map = Basemap(llcrnrlon=-20.0,llcrnrlat=5,urcrnrlon=120,urcrnrlat=50,lat_ts=20,resolution='l',projection='merc')
# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)
map.drawmapboundary(fill_color='#99ffff',zorder=0)
map.fillcontinents(color='#cc9966',lake_color='#99ffff',zorder=1)

# draw lat/lon grid lines every 10 degrees.
#map.drawmeridians(np.arange(0,180,10))
#map.drawparallels(np.arange(-60,60,10))
# draw points for most polluted cities
map.scatter(lons,lats,latlon=True,marker='o',edgecolors='k', facecolors='r',s=pm10,alpha=0.8,zorder=2)


# compute native map projection coordinates of lat/lon grid.
#x, y = map(lons*180./np.pi, lats*180./np.pi)
# contour data over the map.
plt.title('Most Polluted Cities by Abundance of Particles of Size 2.5 - 10 $\mu$m')
plt.text(-500000,-400000,'Data from WHO: http://www.who.int/phe/health_topics/outdoorair/databases/cities-2011/en/')
plt.show()


