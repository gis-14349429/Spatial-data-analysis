"""
Understanding GIS: Assessment 2
@author [14349429]
"""
from time import perf_counter

# set start time
start_time = perf_counter()	

# --- NO CODE ABOVE HERE ---


from geopandas import read_file, GeoSeries
from rasterio import open as rio_open
from numpy.random import uniform
from shapely.geometry import Point
from rasterio.transform import rowcol
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.pyplot import subplots, savefig
from rasterio.plot import show as rio_show
from skimage.draw import disk

    #Importing files
tweets_dataset = read_file("C:/Users/User/OneDrive - The University of Manchester/UGIS/GitHub/ugis-assessment2/data/wr/level3-tweets-subset.shp")
gm_districts = read_file("C:/Users/User/OneDrive - The University of Manchester/UGIS/GitHub/ugis-assessment2/data/wr/gm-districts.shp")
with rio_open ("C:/Users/User/OneDrive - The University of Manchester/UGIS/GitHub/ugis-assessment2/data/wr/100m_pop_2019.tif") as pop:
    pop_data = pop.read(1)
    transform = pop.transform
 #Matching the coordinate system
tweets_dataset = tweets_dataset.to_crs(gm_districts.crs)
#Creating output surfaces
rows = pop_data.shape[0]
cols = pop_data.shape[1]
outputSurface = [[0.0 for _ in range(cols)] for _ in range(rows)]
 
def weighted_redistribution (w,s):       
    #Creating an empty list
    tweet_points = tweets_dataset
    #Looping over each administrative area
    for idx, admin in gm_districts.iterrows():
        
        #Geometry of the admin
        geom = admin.geometry 
        
        #Get the bounds radius of the admin
        minx, miny, maxx, maxy = geom.bounds
        
        #Bounding radius
        br = max(maxx-minx, maxy-miny)/2
        
        #Select points within this polygon
        tweet_points_in_admin = tweet_points[tweet_points.within(geom)]
        if tweet_points_in_admin.empty:
            continue
        
        for _, points in tweet_points_in_admin.iterrows():
            #Initialize the population value
            highest_pop = -float("inf")
            best_location = None
            
            #Checking multiple random locations inside the polygon
            for spot in range(100):
                x = uniform(low=minx, high=maxx)
                y = uniform(low=miny, high=maxy)
                random_point = Point(x,y)
            
                #Checking if the point actually falls inside the district
                if geom.contains(random_point):
                    row,col = rowcol(transform,random_point.x,random_point.y)
                    if 0 <= row < rows and 0 <= col < cols:
                        pop_value = pop_data[row][col]
                        if pop_value > highest_pop:
                            highest_pop = pop_value
                            best_location = random_point
                            
                if best_location is not None:
                    break
            #If no valid point is found
            if best_location is None:
                best_location = geom.centroid
                
            #Computing spatial ambiguity 
            row,col = rowcol(transform, best_location.x,best_location.y)
            radius = int(s * (geom.area / 3.14) ** 0.5 / abs(transform.a))
                
            #Drawing a circle
            r,c = disk ((row,col),radius,shape=(rows,cols))
            for r_idx, c_idx in zip(r,c):
                outputSurface[r_idx][c_idx] += w
    return outputSurface
    
        
       
        

        
  




# --- NO CODE BELOW HERE ---

# report runtime
print(f"completed in: {perf_counter() - start_time} seconds")