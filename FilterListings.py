# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 14:28:34 2020

@author: eachr
"""

# =============================================================================
# Sample dict
# {'bedroom': '2+', 
#  'bathroom': '2+', 
#  'propertyTypeName': 'Condo', 
#  'housePriceName': 'Greater than $100k', 
#  'neighbourhoodfactors': '3somewhatimportant', 
#  'distance': '5.0'} 
# =============================================================================

fake_dict = {'bedroom': '2+', 
  'bathroom': '1+', 
  'propertyTypeName': 'Condo', 
  'housePriceName': 'Greater than $100k', 
  'neighbourhoodfactors': '3somewhatimportant', 
  'distance': '5.0'}

def PropertyFilter(value_dict):
    import pandas as pd
    
    ## pull correct dataset
    
    listings = "Updated Listings within %s miles.csv"
    walk = "Updated Listings within 0.5 miles.csv"
    walk_bike = "Updated Listings within 2.5 miles.csv"
    car = "Updated Listings within 5.0 miles.csv"
    
    def digit_extractor(value):
        #Simple function to match digit patterns and extract those numerics
        # Currently doesn't support comma-formatted numbers
        import re
        
        digit = float(re.search("\d+(\.\d+)*", value)[0])
        if digit:
            return digit
        else: 
            return 0
    
    ## find which listing we are working with 
    listing_dist = float(digit_extractor(value_dict['distance']))
    listing_csv=  listings %(listing_dist)
    
    dat = pd.read_csv(listing_csv)
    
    ## filters
    # Extract digits from dictionary values
    bedrooms = digit_extractor(value_dict['bedroom'])
    bathrooms = digit_extractor(value_dict['bathroom'])
    propType = [value_dict['propertyTypeName'].lower()]
    price = digit_extractor(value_dict['housePriceName']) * 1000
    
    if price == 0:
        price = 9999999999999999999
        
    if propType == 'any':
        propType = list(dat.prop_type.unique())
    
    f_dat = dat[(dat['beds'] >= bedrooms) & 
                (dat['baths'] >= bathrooms) &
                (dat['price'] <= price) &
                (dat['prop_type'].isin(propType))]
    
    if len(f_dat) == 0:
        raise Exception("There are no listings that fit your criteria")
    
    return f_dat
    
    
    
m= PropertyFilter(fake_dict)