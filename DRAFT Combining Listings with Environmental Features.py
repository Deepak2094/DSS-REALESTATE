# Aggregating Environmental Features by Distance

# I hard coded this to only check count of locations within radius and median rating 

import pandas as pd
from haversine import haversine, Unit

## = UPDATE = ##
radius = 1.0 # in miles
listings =  pd.read_csv("") # data for real estate listings
locations = pd.read_csv("") # data for environmental features of locations, i.e. restaurants
## ========== ##

# Calculate distance between 2 points
def calc_dist(listing_coordinates, location_coordinates): # coordinates are in format string "lat,long"
    listing_coordinates, location_coordinates = tuple([float(x) for x in listing_coordinates.split(",")]), tuple([float(x) for x in location_coordinates.split(",")])
    distance = haversine(listing_coordinates,location_coordinates, unit=Unit.MILES)
    return distance

# Aggregate count of locations and median rating within distance radius
def aggregate_env_info():
    # deep copy original dfs
    temp_locations = locations.copy(deep=True)
    temp_listings = listings.copy(deep=True)
    # iterate through listings coordinates
    for idx, listing_coordinates in temp_listings['LatLong'].iteritems():
        # For each listings coordinate, calculate the distance to each location and add to [distance, rating] to results df
        temp_locations["Distance_from_listing"] = [calc_dist(listing_coordinates, x) for x in temp_locations['LatLong']]
        results = pd.DataFrame([[x,y] for (x,y) in zip(temp_locations["Distance_from_listing"],temp_locations["Rating"]) if x <= radius ],columns=["Distance","Rating"])
        # aggregate results
        count = len(results)
        med = results["Rating"].median()
        # Update new column in listing at the index of the original coordinates
        temp_listings.at[idx, 'Num_Restaurants'] = count
        temp_listings.at[idx, 'Median_Rating'] = med
    return temp_listings

test = aggregate_env_info()
