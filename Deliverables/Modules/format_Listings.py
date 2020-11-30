""" This file conatins the user defined function to format the Listings for Landing Page """
import random
import pandas as pd


def random_phone_num_generator():
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    while last in ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888']:
        last = (str(random.randint(1, 9998)).zfill(4))
    return '{}-{}-{}'.format(first, second, last)


Agent_data = pd.read_csv("../Inputs/Agents.csv")


def random_agent(df):
    agent_name = random.choice(df["agent_name"].tolist())
    agent_office = random.choice(df["agent_office"].tolist())
    return [agent_name, agent_office]


def format_Listings(Listings_dict):
    variable_dict = {}
    for i in range(1, 7):
        variable_dict[f"Rank{i}_thumbnail"] = Listings_dict["thumbnail"][i]
        variable_dict[f"Rank{i}_agent_name"] = random_agent(Agent_data)[0]
        variable_dict[f"Rank{i}_agent_office"] = random_agent(Agent_data)[1]
        variable_dict[f"Rank{i}_phnumber"] = random_phone_num_generator()
        variable_dict[f"Rank{i}_Price"] = "{:,}".format(int(Listings_dict["price"][i]))
        variable_dict[f"Rank{i}_beds"] = int(Listings_dict["beds"][i])
        variable_dict[f"Rank{i}_baths"] = int(Listings_dict["baths"][i])
        variable_dict[f"Rank{i}_size"] = "{:,}".format(int(Listings_dict["size_in_sqft"][i]))
        variable_dict[f"Rank{i}_address"] = Listings_dict["Line"][i]
        variable_dict[f"Rank{i}_School"] = Listings_dict["NearestSchools"][i]
        variable_dict[f"Rank{i}_Metro"] = (
                Listings_dict["NearestMetro"][i] + "-" + str(round(Listings_dict["MetroDistance"][i], 1)))
        variable_dict[f"Rank{i}_BusStop"] = round(Listings_dict["BusDistance"][i], 1)
        variable_dict[f"Rank{i}_CommunityCenter"] = Listings_dict["NearestCC"][i]
        variable_dict[f"Rank{i}_Library"] = Listings_dict["NearestLIB"][i]
        variable_dict[f"Rank{i}_Restaurant"] = ','.join(
            [str(elem) for elem in Listings_dict["Top_5_Rated_restaurants"][i].split(';')[0:3]])

        variable_dict[f"Rank{i}_Bars"] = ','.join(
            [str(elem) for elem in Listings_dict["Top_5_Rated_bars"][i].split(';')[0:3]])
    # variable_dict[f"Rank{i}_MoreRestaurants"] = ','.join(
    #     [str(elem) for elem in Listings_dict["Top_5_Rated_restaurants"][i].split(';')[1:]])
    # variable_dict[f"Rank{i}_MoreBars"] = ','.join(
    #     [str(elem) for elem in Listings_dict["Top_5_Rated_bars"][i].split(';')[1:]])
    return variable_dict
