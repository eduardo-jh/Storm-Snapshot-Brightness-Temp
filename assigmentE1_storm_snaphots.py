# -*- coding: utf-8 -*-
""" ATMO555 Assignment E1. Brightness temperature from netCDF4 file, 8/30/2021
@author: eduardo
"""
from osgeo import gdal
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

THRESHOLD = 180 # Remove data below this temp (in Kelvin)

# Open the netCDF4 file
dr = 'DATA/'
fn = 'merg_2021082103_4km-pixel.nc4'
ds = gdal.Open(dr + fn)

# Explore the datasets within the file
print("Datasets:")
for item in ds.GetSubDatasets():
    print(item[0])

# Open the subdataset in the format 'NETCDF:"DATA/merg_2021082103_4km-pixel.nc4":Tb'
tb = gdal.Open(ds.GetSubDatasets()[0][0])  # First subdataset from the first dataset

# Show some metadata
for key, value in tb.GetMetadata().items():
    print("{:35}: {}".format(key, value))
print('Band shape (T, Y, X): ', (tb.RasterCount, tb.RasterYSize, tb.RasterXSize))
print('Projection: ', tb.GetProjection())

# Get the geotransform metadata (extension) of the figure to scale the figure
geoTransform = tb.GetGeoTransform()
print(geoTransform)
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * tb.RasterXSize
miny = maxy + geoTransform[5] * tb.RasterYSize
print("Spatial extent [minx,miny,maxx,maxy]: ", [minx, miny, maxx, maxy])

# Extract the temperature matrix data
data = tb.ReadAsArray(0, 0, tb.RasterXSize, tb.RasterYSize)
# data[data < THRESHOLD] = THRESHOLD  # Remove data below threshold

# Create a figure and plot a coastline 
plt.figure(figsize=(12,12))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
# ax.set_xticks([-180,-90,0,90,180])
# ax.set_yticks([-60,0,60])

# Plot the temperature matrix data and save the figure
# plt.imshow(data[0])
plt.imshow(data[0], extent=[minx,maxx,miny,maxy], cmap='RdYlBu_r') # This has two times: 0 or 1
plt.title(fn)
# plt.colorbar(orientation='horizontal', pad=0.03)
# # plt.savefig('snapshot_' + fn[:-4] + '.png', dpi=300, bbox_inches='tight')

# # Zoom to the hurricane
# plt.ylim(10, 30)
# plt.xlim(-120, -80)
# plt.savefig('snapshot_' + fn[:-4] + '_zoom.png', dpi=300, bbox_inches='tight')

plt.show()