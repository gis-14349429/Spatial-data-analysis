"""
Understanding GIS: Assessment 2
@author [14349429]
"""
from time import perf_counter

# set start time
start_time = perf_counter()	

# --- NO CODE ABOVE HERE ---
from geopandas import read_file
from rasterio import open as rio_open
from numpy import zeros
from numpy.random import uniform
from shapely.geometry import Point

#Importing files
tweets_dataset = read_file("../../../../../../data/wr/level3-tweets-subset.shp")
gm_districts = read_file("../../../../../../data/wr/gm-districts.shp")
with rio_open ("../../../../../../data/wr/100m_pop_2019.tif") as pop:
    pop_data = pop.read(1)
    
#Matching the coordinate system
tweets_dataset = read_file("../../../../../../data/wr/level3-tweets-subset.shp").to_crs(gm_districts)

#Creating empty output surfaces
outputSurface = zeros.twitter_activity(pop_data)

#Creating an empty list
tweet_points = []

for idx, admin in gm_districts.iterrows():
    
    #Geometry of the admin
    geoms = admin.geometry 
    
    #Geometric centroid of the admin 
    centroid = geoms.centroid
    
    #Get the bounds radius of the admin
    minx, miny, maxx, maxy = geoms.bounds
    
    #Calculate the required number of random locations
    sample_number = 1000
    while True:
        xs = uniform (low=minx, high=maxx, size=sample_number)
        ys = uniform (low=minx, high=maxx, size=sample_number)
        random_point = Point(xs, ys)
        if geoms.bounds.contains(random_point):
            tweet_points.append(random_point)
        #Exit when list length == n
        if len(tweet_points) == sample_number: 
            break
            













# --- NO CODE BELOW HERE ---

# report runtime
print(f"completed in: {perf_counter() - start_time} seconds")