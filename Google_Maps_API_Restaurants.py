# SYST 542
# Script for pulling restaurant data within a mile (1600 meters) from a lat,long point
import pandas as pd
import json
import urllib.request
import numpy as np

## UPDATE ## 
# your Google Maps API key
your_key = ""

# dictionary object of "area" and their latitudes and longitudes you want to look at
# add whatever you want
locations = {"Columbia Pike":"38.862579,-77.086907",
             "Bailey's Crossroads":"38.852122,-77.129442",
             "Patomac Yard":"38.835779,-77.050375",
             "Seven Corners": "38.869086,-77.145591"
             }

# path for Arlington metro stop locations ("Text Search" fuctionality)
metro_path = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=metro+stops+Arlington+VA&key="+your_key

## UPDATE ## Change type= "bar", "cafe", etc.
# path for the first page of restaurant search results ("Search Nearby" functionality)
original_path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=latlong&radius=1600&type=restaurant&key="+your_key


# pulls JSON from google API into a dictionary
def pull_data(path):
    with urllib.request.urlopen(path) as url:
        data = json.loads(url.read().decode())
    return data

# You can only access 20 results at a time. Any more are added to another page
# (up to 2 additional pages)
# checks if JSON has a "next page" field and 
def check_next_page(data):
    try:
        next_page_token = data["next_page_token"]
        next_page_path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken="+next_page_token+"&key="+your_key
        return next_page_path
    except:
        return False

# return latitude/longitude from the geometry portion of each result
def extract_latlong(location_result):
    location = location_result["geometry"]["location"]
    latlong = str(location["lat"])+","+str(location["lng"])
    return latlong

# free text Google search for metros in Arlington VA, ignore any not in VA, and update locations dictionary       
#
# NOTE: I didn't bother cleaning any similar search results ("Ballston" vs "Ballston Metro") because it was only 20 results
def populate_locations():
    metro_data = pull_data(metro_path)
    for location in metro_data["results"]:
        if "VA" in location["formatted_address"]:
            locations.update({location["name"]:extract_latlong(location)})
    # check if there are any additional pages
    next_page = check_next_page(metro_data)
    while check_next_page(next_page) != False:
        next_page = pull_data(next_page)
        for location in next_page["results"]:
            if "VA" in location["formatted_address"]:
                locations.update({location["name"]:extract_latlong(location)})

# add VA metro stops to locations dictionary
populate_locations()

# create a dataframe of restaurants (or whatever type of store/facility you want) and their features
# does a Google API search for restaurants in a 1 mile radius of every location in the locations dictionary
def create_restaurants_df():
    print("")
    print("Retrieving data from API...")
    print("")
    urls_to_pull = []
    data_to_add = []
    # Create a url for each location based on its latlong
    for area in locations:
        location_path = original_path.replace("latlong",locations[area])
        urls_to_pull.append(location_path)
    # For each url, pull the data. Append relevant fields to data_to_add list
    for path in urls_to_pull:
        data = pull_data(path)
        for restuarant in data["results"]:
            ## UPDATE ## Change fields relevant to your dataset
            try:
                rating = restuarant["rating"]
            except:
                rating = np.NaN
            try:
                price_level = restuarant["price_level"]
            except:
                price_level = np.NaN
            entry = [restuarant["name"], restuarant["vicinity"], price_level,rating,restuarant["business_status"],extract_latlong(restuarant)]
            data_to_add.append(entry)
        # Check if there's a Next Page option and add it to the list of urls to pull
        next_page = check_next_page(data)
        if next_page != False:
            urls_to_pull.append(next_page)
    ## UPDATE ## Change column names as needed
    df=pd.DataFrame(data_to_add,columns=['RestaurantName','AddressVicinity','PriceLevel','Rating','BusinessStatus','LatLong'])
    return df
        
restaurants_df = create_restaurants_df()

# drop duplicates and save as CSV
restaurants_df = restaurants_df.drop_duplicates()
## UPDATE ##  Add your local file path
local_path = ""
restaurants_df.to_csv(local_path)
    
