# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 16:49:00 2020

@author: eachr
"""

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
locations = {"Rivercrest": "38.9226,-77.1190",
             "Greenbier Park": "38.9010,-77.1402",
             "Bishop O'Connell HS": "38.894753,-77.161094",
             "Westover Park": "38.8828017,-77.1271647",
             "Glencarlyn" : "38.864455,-77.124052",
             "Barcroft Forest" : "38.8488,-77.1020",
             "Village at Shirlington": "38.8411,-77.0869",
             "Army Navy Golf Course": "38.85130,-77.07929",
             "Auora Hills": "38.8515,-77.0641",
             "Crystal City": "38.8554,-77.0521",
             "Pentagon" : "38.8719,-77.0563",
             "Rosslyn" : "38.8940,-77.0752",
             "Lyon Village" : "38.893343,-77.094429",
             "Cherrydale" : "38.900636,-77.107479",
             "Bellevue Forest": "38.9165,-77.1154",
             "Highview Park" : "38.8941,-77.1277",
             "Ballston": "38.8858,-77.1054",
             "Alcova Heights": "38.8644,-77.0974",
             "Columbia Heights": "38.864395,-77.079549",
             "Clarendon":"38.8859,-77.0969",
             "Columbia Pike":"38.862579,-77.086907",
             "Patomac Yard":"38.835779,-77.050375",
             "Seven Corners": "38.869086,-77.145591"
             }

# path for Arlington metro stop locations ("Text Search" fuctionality)
#metro_path = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=metro+stops+Arlington+VA&key="+your_key

## UPDATE ## Change type= "bar", "cafe", etc.
# path for the first page of restaurant search results ("Search Nearby" functionality)
original_path = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=latlong&radius=2000&type=bus_station&key="+your_key


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
def create_bars_df():
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
        for bar in data["results"]:
            ## UPDATE ## Change fields relevant to your dataset
            try:
                rating = bar["rating"]
            except:
                rating = np.NaN
            try:
                price_level = bar["price_level"]
            except:
                price_level = np.NaN
            entry = [bar["name"], bar["vicinity"], price_level,rating,bar["business_status"],extract_latlong(bar)]
            data_to_add.append(entry)
        # Check if there's a Next Page option and add it to the list of urls to pull
        next_page = check_next_page(data)
        if next_page != False:
            urls_to_pull.append(next_page)
    ## UPDATE ## Change column names as needed
    df=pd.DataFrame(data_to_add,columns=['BarName','AddressVicinity','PriceLevel','Rating','BusinessStatus','LatLong'])
    return df

def create_buses_df():
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
        for bus in data["results"]:
            ## UPDATE ## Change fields relevant to your dataset
            entry = [bus["name"], bus["vicinity"],extract_latlong(bus)]
            data_to_add.append(entry)
        # Check if there's a Next Page option and add it to the list of urls to pull
        next_page = check_next_page(data)
        if next_page != False:
            urls_to_pull.append(next_page)
    ## UPDATE ## Change column names as needed
    df=pd.DataFrame(data_to_add,columns=['BusStopName','AddressVicinity','LatLong'])
    return df
        
bars_df = create_bars_df()
bars_df.to_csv("../barsRaw.csv")

# drop duplicates and save as CSV
bars_df_clean = bars_df.drop_duplicates()
## UPDATE ##  Add your local file path
local_path = ""
bars_df_clean.to_csv("../barsClean.csv")

bus_df = create_buses_df()
bus_df.to_csv("busRaw.csv")
#bus_df = pd.read_csv("busRaw.csv")

bus_df_clean = bus_df.drop_duplicates(subset = ['BusStopName'])
## UPDATE ##  Add your local file path
local_path = ""
bus_df_clean.to_csv("busClean.csv")
