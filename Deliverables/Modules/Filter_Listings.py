"""
Created on Sun Nov  1 14:28:34 2020
@author: eachr
"""

# =============================================================================
# Sample dict
# {'bedroom': 'Any',
# 'bathroom': 'Any', 
# 'propertyTypeName': 'Any', 
# 'housePriceName': 'Any', 
# 'neighbourhoodfactors': '3somewhatimportant', 
# 'HouseSize': '3somewhatimportant', 
# 'Housebudget': '3somewhatimportant', 
# 'BusStop': '3somewhatimportant', 
# 'Metro': '3somewhatimportant', 
# 'Restaurants': '3somewhatimportant', 
# 'Bars': '3somewhatimportant', 
# 'School_quality': '3somewhatimportant', 
# 'CommunityCenter': '3somewhatimportant', 
# 'Library': '3somewhatimportant', 
# 'distance': '5.0'}
#
# =============================================================================

samp_dict = {'bedroom': '2+',
             'bathroom': 'Any',
             'propertyTypeName': 'Single Family Home',
             'housePriceName': 'Any',
             'neighbourhoodfactors': '3somewhatimportant',
             'HouseSize': '3somewhatimportant',
             'Housebudget': '3somewhatimportant',
             'BusStop': '3somewhatimportant',
             'Metro': '3somewhatimportant',
             'Restaurants': '3somewhatimportant',
             'Bars': '3somewhatimportant',
             'School_quality': '3somewhatimportant',
             'CommunityCenter': '3somewhatimportant',
             'Library': '3somewhatimportant',
             'distance': '5.0'}


def PropertyFilter(page1_dict):
    import pandas as pd

    ## pull correct dataset

    listings = "Updated Listings within %s miles.csv"
    walk = "Updated Listings within 0.5 miles.csv"
    walk_bike = "Updated Listings within 2.5 miles.csv"
    car = "Updated Listings within 5.0 miles.csv"

    def digit_extractor(value):
        # Simple function to match digit patterns and extract those numerics
        # Currently doesn't support comma-formatted numbers
        import re

        digit = re.search("\d+(\.\d+)*", value)
        if digit:
            return float(digit[0])
        else:
            return 0

    ## find which listing we are working with 
    listing_dist = float(digit_extractor(page1_dict['distance']))
    listing_csv = listings % (listing_dist)

    dat = pd.read_csv("Inputs/"+listing_csv)

    ## filters
    # Extract digits from dictionary values
    bedrooms = digit_extractor(page1_dict['bedroom'])
    bathrooms = digit_extractor(page1_dict['bathroom'])
    price = digit_extractor(page1_dict['housePriceName']) * 1000

    page1_dict['propertyTypeName'] = page1_dict['propertyTypeName'].replace(" Home", "")
    propType = [page1_dict['propertyTypeName'].lower().replace(" ", "_")]

    if price == 0:
        price = 9999999999999999999

    if propType == ['any']:
        propType = list(dat.prop_type.unique())

    f_dat = dat[(dat['beds'] >= bedrooms) &
                (dat['baths'] >= bathrooms) &
                (dat['price'] <= price) &
                (dat['prop_type'].isin(propType))]

    if len(f_dat) == 0:
        raise Exception("There are no listings that fit your criteria")

    return f_dat


m = PropertyFilter(samp_dict)