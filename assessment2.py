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
from numpy.random import uniform
from shapely.geometry import Point
from rasterio.transform import rowcol

#Importing files
tweets_dataset = read_file("C:/Users/User/OneDrive - The University of Manchester/UGIS/GitHub/ugis-assessment2/data/wr/level3-tweets-subset.shp")
gm_districts = read_file("C:/Users/User/OneDrive - The University of Manchester/UGIS/GitHub/ugis-assessment2/data/wr/gm-districts.shp")
with rio_open ("C:/Users/User/OneDrive - The University of Manchester/UGIS/GitHub/ugis-assessment2/data/wr/100m_pop_2019.tif") as pop:
    pop_data = pop.read(1)
    transform = pop.transform
    
#Matching the coordinate system
tweets_dataset = tweets_dataset.to_crs(gm_districts.crs)

#Creating empty output surfaces
rows = pop_data.shape[0]
cols = pop_data.shape[1]
outputSurface = [[0.0 for _ in range(cols)] for _ in range(rows)]

for idx, admin in gm_districts.iterrows():
    
    #Geometry of the admin
    geom = admin.geometry 
    
    #Geometric centroid of the admin 
    centroid = geom.centroid
    
    #Get the bounds radius of the admin
    minx, miny, maxx, maxy = geom.bounds
    
    #Tweets belonging to this district
    district_tweets = tweets_dataset[tweets_dataset.within(geom)]
    
    for _, tweet in district_tweets.iterrows():
        
        #Creating an empty list
        tweet_points = []
        
        #Calculate the required number of random locations
        sample_number = 1000
        while len(tweet_points) < sample_number:
            x = uniform (low=minx, high=maxx)
            y = uniform (low=miny, high=maxy)
            random_point = Point(x, y)
            if geom.contains(random_point):
                tweet_points.append(random_point)
            
        highest_pop = float("-inf")
        best_location = None

        for p in tweet_points:
            row, col = rowcol(transform, p.x, p.y)
            
            if 0 <= row < pop_data.shape[0] and 0 <= col < pop_data.shape[1]:
                location = pop_data[row][col]
                if location > highest_pop:
                    highest_pop = location 
                    best_location = p
        if best_location is not None:
            row, col = rowcol(transform, best_location.x, best_location.y)
            outputSurface[row][col] += 1
    
    
        
            











# --- NO CODE BELOW HERE ---

# report runtime
print(f"completed in: {perf_counter() - start_time} seconds")