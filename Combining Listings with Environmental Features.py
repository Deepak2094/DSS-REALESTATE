# Aggregating Environmental Features by Distance
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from haversine import haversine, Unit

## = UPDATE = ##
path = r"C:\Users\eachr\Documents\GMU Fall 2020\SYST 542\Project\Code\DSS-REALESTATE-master"
listings =  pd.read_csv(path+r"\Real_Estate_Listings.csv") # data for real estate listings
restaurants = pd.read_csv(path+r"\Arlington Restaurants V2.csv")
bars = pd.read_csv(path+r"\barsClean.csv")
buses = pd.read_csv(path+r"\busClean.csv")
school_ratings = pd.read_csv(path+r"\schoolsClean.csv")
arlDat = pd.read_csv(path+r"\Facility_Points.csv")

## +++++++++ DATA PROCESSING +++++++++ ###

##Prep Data
buses.rename(columns = {"Unnamed":"Index", "BusStopName":"NAME", "AddressVicinity":"Address", "LatLong":"point_LatLong"}, inplace= True)
#arlDat.rename(columns = {"Unnamed":"Index", "LatLong":"point_LatLong"}, inplace= True)

### Several Arl Data Addresses are incorrect to pull Lat Long
### Manual fix bc thats just the way it is


arlDat['ADDRESS'].replace(['5800 N WASHINGTON BLVD'], '5800 WASHINGTON BLVD', inplace = True)
arlDat['ADDRESS'].replace(['4200 S FOUR MILE RUN'], '4200 S FOUR MILE RUN DR', inplace = True)
arlDat['ADDRESS'].replace(['2121 CULPEPER ST'], '2121 N CULPEPER ST', inplace = True)
arlDat['ADDRESS'].replace(['2 S ROTARY RD'], 'Pentagon Metro Station', inplace = True)
arlDat['ADDRESS'].replace(['2400 S SMITH BLVD'], '2400 SMITH BLVD', inplace = True)
arlDat['ADDRESS'].replace(['2190 N MILITARY RD'], '2190 MILITARY RD', inplace = True)
arlDat['ADDRESS'].replace(['1644 MCKINLEY RD'], '1644 N MCKINLEY RD', inplace = True)
#arlDat['ADDRESS'].replace(['5800 N WASHINGTON BLVD'], '5800 WASHINGTON BLVD', inplace = True)
#arlDat['ADDRESS'].replace(['5800 N WASHINGTON BLVD'], '5800 WASHINGTON BLVD', inplace = True)

##Add coodrinates to Arlington Features


def get_coords(address_str,locator):
    loc = locator.geocode(address_str)
    try:
        ret = loc.raw['lat']+"," + loc.raw['lon']
    except:
        ret = None
    return ret

## Adding LatLong Points

    # Adding "LatLong" field
listings["LatLong"] = listings["lat"].astype(str)+","+listings["lon"].astype(str)
    # Dropping "land" options
listings = listings[listings.prop_type != "land"]

### Mining Arlington Data for Coordinates
geolocator = Nominatim(user_agent="myGeocoder", timeout = 30)
arlDat['ADDRESS'] = arlDat['ADDRESS'].astype(str)+", Arlington, VA"
arlDat['point_LatLong'] = arlDat['ADDRESS'].apply(get_coords, locator = geolocator)

### Manually add coords of two more points that couldn't be found
arlDat.loc[arlDat.NAME == "National Airport Metro", 'point_LatLong'] = "38.8536,-77.0441"
arlDat.loc[arlDat.NAME == "Dorothy Hamm Middle School", 'point_LatLong'] = "38.900490,-77.111214"
## +++++++++  SPLIT OUT ARL DATA +++++++ ####

#arlDat.to_csv("arlData_CLEANED.csv")
community = arlDat[arlDat.SYMBOL == "CC"]
libraries = arlDat[arlDat.SYMBOL == "LB"]
metro = arlDat[arlDat.SYMBOL.str.contains('M[^S]', regex= True, na=False)]
schools = arlDat[arlDat.SYMBOL.str.contains('(ES|AES|MS|HS)', regex= True, na=False)]



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


# Search Alg to pull minimum index point
def find_nearest(coords, InterestPoint):
    
    distances = InterestPoint.apply(
        lambda row: calc_dist(coords, row['point_LatLong']), axis = 1)
    
    return InterestPoint.loc[distances.idxmin(),'NAME']

# Add distances to data frame
def calculate_distances(locations, listings, featuretype):
    
    newColName = "Nearest" + featuretype
    
    temp = listings
    temp[newColName] = temp.apply(
        lambda row: find_nearest(row['LatLong'], locations), 
        axis=1)
    
    temp = pd.merge(temp, locations[['NAME','point_LatLong']], left_on = newColName,right_on = 'NAME', how ='left')
    
    temp[featuretype+"Distance"] = [calc_dist(temp.LatLong[i], temp.point_LatLong[i]) for i in range(len(temp))]
    
    temp[featuretype+"Distance" ] = temp[featuretype+"Distance"] .round(decimals = 3)
    
    temp.drop(['point_LatLong', 'NAME'], axis = 1, inplace = True)
    
    
    return temp


### Add different Feature Distances and Names to listings
listings2 = calculate_distances(buses,listings,"Bus")
listings2 = calculate_distances(metro,listings2,"Metro")
listings2 = calculate_distances(community,listings2,"CC")
listings2 = calculate_distances(libraries,listings2,"LIB")
listings2 = calculate_distances(schools,listings2,"Schools")

## add ratings
listings_f = listings2.merge(school_ratings[['NAME','RATING']], how = 'left' , left_on = 'NearestSchools', right_on = "NAME").drop(['NAME'], axis = 1)
#listings2 = calculate_distances(buses,listings2,"Bus")

for radius in [0.5, 1.0,2.5,5.0]:
    updated_listings = aggregate_env_info(bars, listings_f,radius,"bars","BarName")
    updated_listings = aggregate_env_info(restaurants,updated_listings, radius,"restaurants","RestaurantName")
    updated_listings.to_csv(path+r"\Updated Listings within "+str(radius)+r" miles.csv")


