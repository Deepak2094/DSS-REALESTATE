import requests
import json
import glob
import pandas as pd

Data = {}
url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"

for count in range(5):
    offset = count * 200 # Paging Feature, offsets the data by 200 rows
    querystring = {"sort": "relevance", "city": "Arlington", "limit": "200", "offset": "{0}".format(offset),
                   "state_code": "VA"}

    headers = {
        'x-rapidapi-host': "realtor.p.rapidapi.com",
        'x-rapidapi-key': "" # Your Rapid API key goes in here
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    temp = json.loads(response.text)
    for k, v in temp.items():
        Data[k] = v

    with open(f'Test{count}.json', 'w') as outfile:
        json.dump(Data, outfile)

Data_Dictionary = {}

property_ID = []
Listing_ID = []
Listing_Url = []
prop_type = []
prop_sub_type = []
city = []
Line = []
postal_code = []
lat = []
lon = []
neighborhood_name = []
price = []
baths_half = []
baths_full = []
baths = []
beds = []
size = []
thumbnail = []
lot_size = []

# Opening the file and filtering for the data we need
for f in glob.glob("Test*.json"):
    with open(f, "r") as read_file:
        Data = json.load(read_file)
        for k, v in Data.items():
            if k == "properties":

                for i in range(len(v)):
                    property_ID.append(Data["properties"][i]["property_id"])
                    Listing_ID.append(Data["properties"][i]["listing_id"])
                    Listing_Url.append(Data["properties"][i]["rdc_web_url"])
                    prop_type.append(Data["properties"][i]["prop_type"])

                    if "prop_sub_type" in Data["properties"][i].keys():
                        prop_sub_type.append(Data["properties"][i]["prop_sub_type"])
                    else:
                        prop_sub_type.append("NA")

                    if "lot_size" in Data["properties"][i].keys():
                        lot_size.append(Data["properties"][i]["lot_size"]["size"])
                    else:
                        lot_size.append("NA")

                    city.append(Data["properties"][i]["address"]["city"])
                    Line.append(Data["properties"][i]["address"]["line"])
                    postal_code.append(Data["properties"][i]["address"]["postal_code"])

                    lat.append(Data["properties"][i]["address"]["lat"])
                    lon.append(Data["properties"][i]["address"]["lon"])

                    if "neighborhood_name" in Data["properties"][i]["address"].keys():
                        neighborhood_name.append(Data["properties"][i]["address"]["neighborhood_name"])
                    else:
                        neighborhood_name.append("NA")

                    price.append(Data["properties"][i]["price"])

                    if "baths_half" in Data["properties"][i].keys():
                        baths_half.append(Data["properties"][i]["baths_half"])
                    else:
                        baths_half.append("NA")

                    if "baths_full" in Data["properties"][i].keys():
                        baths_full.append(Data["properties"][i]["baths_full"])
                    else:
                        baths_full.append("NA")

                    baths.append(Data["properties"][i]["baths"])
                    beds.append(Data["properties"][i]["beds"])

                    if "building_size" in Data["properties"][i].keys():
                        size.append(Data["properties"][i]["building_size"]["size"])
                    else:
                        size.append("NA")

                    if "thumbnail" in Data["properties"][i].keys():
                        thumbnail.append(Data["properties"][i]["thumbnail"])
                    else:
                        thumbnail.append("NA")

Data_Dictionary["property_ID"] = property_ID
Data_Dictionary["Listing_ID"] = Listing_ID
Data_Dictionary["price"] = price
Data_Dictionary["baths_half"] = baths_half
Data_Dictionary["baths_full"] = baths_full
Data_Dictionary["baths"] = baths
Data_Dictionary["beds"] = beds
Data_Dictionary["size_in_sqft"] = size
Data_Dictionary["lot_size_in_sqft"] = lot_size
Data_Dictionary["prop_type"] = prop_type
Data_Dictionary["prop_sub_type"] = prop_sub_type
Data_Dictionary["city"] = city
Data_Dictionary["Line"] = Line
Data_Dictionary["postal_code"] = postal_code
Data_Dictionary["lat"] = lat
Data_Dictionary["lon"] = lon
Data_Dictionary["neighborhood_name"] = neighborhood_name
Data_Dictionary["Listing_Url"] = Listing_Url
Data_Dictionary["thumbnail"] = thumbnail

df = pd.DataFrame(Data_Dictionary)
df.to_csv("Real_Estate_Listings_Test.csv", index=False)
