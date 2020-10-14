# Aggregating Environmental Features by Distance
import pandas as pd
from haversine import haversine, Unit

## = UPDATE = ##
path = r""
listings =  pd.read_csv(path+r"\Real_Estate_Listings.csv") # data for real estate listings
restaurants = pd.read_csv(path+r"\Arlington Restaurants V2.csv")
bars = pd.read_csv(path+r"\barsClean.csv")
## ========== ##

# Calculate distance between 2 points
def calc_dist(listing_coordinates, location_coordinates): # coordinates are in format string "lat,long"
    listing_coordinates, location_coordinates = tuple([float(x) for x in listing_coordinates.split(",")]), tuple([float(x) for x in location_coordinates.split(",")])
    distance = haversine(listing_coordinates,location_coordinates, unit=Unit.MILES)
    return distance

# Aggregate count of locations and mean rating within distance radius
def aggregate_env_info(locations, listings, radius,label,name_field): # locations, real estate listings df,
    # deep copy original dfs
    temp_locations = locations.copy(deep=True)
    temp_listings = listings.copy(deep=True)
    # iterate through listings coordinates
    for idx, listing_coordinates in temp_listings['LatLong'].iteritems():
        # For each listings coordinate, calculate the distance to each location and add to [distance, rating] to results df
        temp_locations["Distance_from_listing"] = [calc_dist(listing_coordinates, x) for x in temp_locations['LatLong']]
        results = pd.DataFrame([[w,x,y,z] for (w,x,y,z) in zip(temp_locations[name_field],temp_locations["Distance_from_listing"],temp_locations["Rating"],temp_locations["PriceLevel"]) if x <= radius],columns=["Name","Distance","Rating","PriceLevel"])
        # aggregate results
        top_5 = "; ".join(list(results.sort_values(by=["Rating","Name"],ascending=[False,True])["Name"][:5]))
        count = len(results)
        mean_rating = results["Rating"].mean()
        mean_price_level = results["PriceLevel"].mean()
        # Update new column in listing at the index of the original coordinates
        temp_listings.at[idx, 'Num_'+label] = count
        temp_listings.at[idx, 'Mean_Rating_'+label] = mean_rating
        temp_listings.at[idx, 'Mean_PriceLevel_'+label] = mean_price_level
        temp_listings.at[idx, 'Top_5_Rated_'+label] = top_5
    return temp_listings

# Adding "LatLong" field
listings["LatLong"] = listings["lat"].astype(str)+","+listings["lon"].astype(str)
# Dropping "land" options
listings = listings[listings.prop_type != "land"]

for radius in [0.5, 1.0,2.5,5.0]:
    updated_listings = aggregate_env_info(bars, listings,radius,"bars","BarName")
    updated_listings = aggregate_env_info(restaurants,updated_listings, radius,"restaurants","RestaurantName")
    updated_listings.to_csv(path+r"\Updated Listings within "+str(radius)+r" miles.csv")
