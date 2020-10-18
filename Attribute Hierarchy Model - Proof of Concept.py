import copy
import pandas as pd

##########################################################
######                                              ######
######          PULL IN USER RESPONSES              ######
######                                              ######
##########################################################

# In this proof of concept, I used test values for user entered ratings

# hard coding the user rating to a numeric value
rating_xwalk = {
        1:0.00,
        2:0.25,
        3:0.50,
        4:0.75,
        5:1.00 
        }

# an example hierarchical structure of responses, based on our attribute hierarcy
sample_responses = {
	"home_features":[4,{
		"price":[5],
		"home_details":[3,{	
			"baths":[2],
			"beds":[5],
			"size_in_sqft":[5]
		}
	]
	}],
	"neighborhood_features":[2,{
		"restaurants":[5,{
			"Num_restaurants":[4],
			"Mean_Rating_restaurants":[2],
			"Mean_PriceLevel_restaurants":[3]
		}],
		"bars":[2,{
			"Num_bars":[1],
			"Mean_Rating_bars":[3],
			"Mean_PriceLevel_bars":[2]
		}]
	}]
}


##########################################################
######                                              ######
######          ASSIGN WEIGHTS TO MODEL             ######
######                                              ######
##########################################################
         
# read in a dictionary with lists as values and the user rating as the 1st element of said list
# distribute the weights of the response and return a new dictionary with the key and weight
def distribute_weights(tmp_dict):
    sum_values = sum([rating_xwalk[tmp_dict[x][0]] for x in tmp_dict]) # crosswalk the ratings to a numeric value and sum them up for that level
    distributed_weights = {}
    for x in tmp_dict:
        if rating_xwalk[tmp_dict[x][0]] == 0: # account for zero division
            weight = 0
        else:
            weight = rating_xwalk[tmp_dict[x][0]]/sum_values
        distributed_weights.update({x:weight}) # assign a weight to the key based on the numeric value / sum of numeric values     
    return distributed_weights

# read in a dictionary from the response structure
# replace the ratings in the dictionary with the weights
def replace_with_weights(responses):
    weights = distribute_weights(responses)
    for item in weights:
        responses[item][0] = weights[item]
    return responses

# recursively assign weights per level of the structure
def recurse(d):
    if type(d)==type({}):
        d = replace_with_weights(d)
        for k in d:
            if type(d[k]) == list and len(d[k])>1:
                recurse(d[k][1])
            else:
                recurse(d[k])
    return d

# recursivley "trickle down" the weights throughout the structure
    # i.e. home_features (.75) * home_details (.25) * baths (.50) == .09375 relative weight for baths
def trickle_down(d):
    if type(d)==type({}):
        for k in d:
            trickle_down(d[k])
    if type(d)==type([]) and len(d)>1:
        for k in d[1]:
            d[1][k][0] = d[0]*d[1][k][0]
        trickle_down(d[1])
    return d

# feed in the responses with ratings and return weights
def return_weights(responses):
    data = copy.deepcopy(responses)
    weights = recurse(data)
    weights = trickle_down(weights)
    return weights

weights = return_weights(sample_responses)

##########################################################
######                                              ######
######       RANK LISTINGS BASED ON WEIGHTS         ######
######                                              ######
##########################################################

listings = pd.read_csv(r"C:\Users\User\Documents\GMU\SYST 542 - Decision Support Systems\Code\Updated Listings within 0.5 miles.csv")

unpacked_weights = {}

# placing new weights into a dictionary
def unpack_weights(d):
    if type(d)==type({}):
        for k in d:
            unpack_weights(d[k])
    if type(d)==type([]) and len(d)>1:
        for k in d[1]:
            unpacked_weights.update({k:d[1][k][0]})
        unpack_weights(d[1])

unpack_weights(weights)

# limited sample listings data to only the fields we have
required_headers = [x for x in unpacked_weights if x in list(listings.columns)]
listings = listings[["Listing_ID"]+required_headers]

# get single dimensional value function (SDVF) for fields where higher values are important
# i.e. higher rating
def high_values_important(min_val, max_val, x):
    if x == min_val:
        sdvf = 0
    else:
        sdvf = (x - min_val)/(max_val - min_val)
    return sdvf

# get single dimensional value function (SDVF) for fields where lower values are important
# i.e. lower price
def low_values_important(min_val, max_val, x):
    if x == max_val:
        sdvf = 0
    else:
        sdvf = (x - max_val)/(min_val - max_val)
    return sdvf

# Apply high value SDVF to a whole field       
def evaluate_high_values(df, series):
    min_val = df[series].min()
    max_val = df[series].max()
    df[series] = df[series].apply(lambda x: high_values_important(min_val, max_val, x))
    return df

# Apply low value SDVF to a whole field   
def evaluate_low_values(df, series):
    min_val = df[series].min()
    max_val = df[series].max()
    df[series] = df[series].apply(lambda x: low_values_important(min_val, max_val, x))
    return df

# Create the ranked listings dataset based on the weights from the user ratings 
def create_ranked_data(df):
    df_final = copy.deepcopy(df)
    high_vals = [x for x in required_headers if x != "price"] # fields where high vals are important
    low_vals = ['price'] # fields where low vals are important
    for col in high_vals:
        df = evaluate_high_values(df, col)
    for col in low_vals:
        df = evaluate_low_values(df, col)
    df['user_value'] = (df[required_headers] * [unpacked_weights[x] for x in required_headers]).sum(axis=1)
    df = evaluate_high_values(df, 'user_value')
    df = df.drop(columns=required_headers)
    df_final = df_final.merge(df, left_on="Listing_ID", right_on='Listing_ID')
    df_final = df_final.sort_values('user_value', ascending=False)
    return df_final

ranked = create_ranked_data(listings)

    
    