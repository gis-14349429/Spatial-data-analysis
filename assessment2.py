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
    
    #Get the bounds radius of the admin
    minx, miny, maxx, maxy = geom.bounds
    
    #Tweets belonging to this district
    district_tweets = tweets_dataset[tweets_dataset.within(geom)]
    
    for _, tweet in district_tweets.iterrows():
        
        #Creating an empty list
        tweet_points = []
        
        #Calculate the required number of random locations
        sample_number = 100
        while len(tweet_points) < sample_number:
            x = uniform (low=minx, high=maxx)
            y = uniform (low=miny, high=maxy)
            #Creating a point from random coordinates
            random_point = Point(x, y)
            #Checking if the point actually falls inside the district
            if geom.contains(random_point):
                #If the points do fall inside the district, keep the valid points
                tweet_points.append(random_point)
        
        #Initialize the population value
        highest_pop = -float("inf")
        #Initialize the location where most tweets generated
        best_location = None

        #Looping through all the locations 
        for p in tweet_points:
            #Converting real world coordinates into raster 
            row, col = rowcol(transform, p.x, p.y)
            #Checking if the point is inside the raster 
            if 0 <= row < pop_data.shape[0] and 0 <= col < pop_data.shape[1]:
                #Extract the population value at the location
                location = pop_data[row][col]
                #Compare with the best location
                if location > highest_pop:
                    highest_pop = location 
                    best_location = p
        #Adding the tweet to the output location
        if best_location is not None:
            row, col = rowcol(transform, best_location.x, best_location.y)
            outputSurface[row][col] += 1
#Creating a map
fig, my_ax = subplots(1,1,figsize=(16,10))
my_ax.set_title("Twitter activity in Greater Manchester")

rio_show(
    outputSurface,
    ax=my_ax,
    transform=transform,
    cmap="hot",
    )

gm_districts.boundary.plot(
    ax=my_ax,
    color='black',
    linewidth=1
    )


# add north arrow
x, y, arrow_length = 0.97, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
    arrowprops=dict(facecolor='black', width=5, headwidth=15),
    ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

# add scalebar
my_ax.add_artist(ScaleBar(dx=100, units="m", location="lower right"))

#Save the image
savefig('./out/twitter_activity_gm.png')




# --- NO CODE BELOW HERE ---

# report runtime
print(f"completed in: {perf_counter() - start_time} seconds")