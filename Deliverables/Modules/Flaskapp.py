"""  This file creates the Flask application reuired to render the Webpage and display the final Listing to user """

from flask import Flask, request, render_template, redirect, flash
from Modules.Filter_Listings import PropertyFilter
from Modules.Model import create_ranked_data
from Modules.format_Listings import format_Listings
import time

app = Flask(__name__)
app.secret_key = 'some_secret'
session_data = {}

start_time = time.time()


@app.route('/')  # HomePage Url - Shows the user the questionnare
def home_page():
    return render_template('DSS_Form_Page_1.HTML')


@app.route('/DSS_Form_Page1', methods=['GET', 'POST'])  # This Url recieves the input from the user
def DSS_Form_Page1():
    filters = request.form.to_dict()
    for k, v in filters.items():
        session_data[k] = v
    return render_template('DSS_Form_Page_2.HTML'), session_data


@app.route('/DSS_Form_Page2', methods=['GET', 'POST'])  # This Url recieves the input from the user
def DSS_Form_Page2():
    Environmental_Features = request.form.to_dict()
    for k, v in Environmental_Features.items():
        session_data[k] = v
    try:
        PropertyFilter(session_data)
    except:
        flash("Oops, we coudn't find any Houses. Please try relaxing your criteria")
        return render_template("DSS_Form_Page_1.HTML")
    else:
        Listings = create_ranked_data(PropertyFilter(session_data), session_data)
        variables = format_Listings(Listings)
        return render_template('Real_Estate_Listings_Dynamic_Final.html',
                               # Filters
                               Property_Type=session_data['propertyTypeName'],
                               Bedroom_Filter=session_data["bedroom"],
                               Bathroom_Filter=session_data['bathroom'],
                               Travel_Mode=int(float(session_data['distance'])),
                               housePrice=session_data['housePriceName'],
                               # Listings
                               Rank1_thumbnail=variables["Rank1_thumbnail"],
                               Rank1_Price=variables["Rank1_Price"],
                               Rank1_beds=variables["Rank1_beds"],
                               Rank1_baths=variables["Rank1_baths"],
                               Rank1_size=variables["Rank1_size"],
                               Rank1_address=variables["Rank1_address"],
                               Rank1_School=variables["Rank1_School"],
                               Rank1_Metro=variables["Rank1_Metro"],
                               Rank1_BusStop=variables["Rank1_BusStop"],
                               Rank1_CommunityCenter=variables["Rank1_CommunityCenter"],
                               Rank1_Library=variables["Rank1_Library"],
                               Rank1_Restaurant=variables["Rank1_Restaurant"],
                               Rank1_Bars=variables["Rank1_Bars"],
                               Rank1_MoreRestaurants=variables["Rank1_MoreRestaurants"],
                               Rank1_MoreBars=variables["Rank1_MoreBars"],
                               Rank1_Agent_name=variables["Rank1_agent_name"],
                               Rank1_phnumber=variables["Rank1_phnumber"],
                               # Rank 2
                               Rank2_thumbnail=variables["Rank2_thumbnail"],
                               Rank2_Price=variables["Rank2_Price"],
                               Rank2_beds=variables["Rank2_beds"],
                               Rank2_baths=variables["Rank2_baths"],
                               Rank2_size=variables["Rank2_size"],
                               Rank2_address=variables["Rank2_address"],
                               Rank2_School=variables["Rank2_School"],
                               Rank2_Metro=variables["Rank2_Metro"],
                               Rank2_BusStop=variables["Rank2_BusStop"],
                               Rank2_CommunityCenter=variables["Rank2_CommunityCenter"],
                               Rank2_Library=variables["Rank2_Library"],
                               Rank2_Restaurant=variables["Rank2_Restaurant"],
                               Rank2_Bars=variables["Rank2_Bars"],
                               Rank2_MoreRestaurants=variables["Rank2_MoreRestaurants"],
                               Rank2_MoreBars=variables["Rank2_MoreBars"],
                               Rank2_Agent_name=variables["Rank2_agent_name"],
                               Rank2_phnumber=variables["Rank2_phnumber"],
                               # Rank 3
                               Rank3_thumbnail=variables["Rank3_thumbnail"],
                               Rank3_Price=variables["Rank3_Price"],
                               Rank3_beds=variables["Rank3_beds"],
                               Rank3_baths=variables["Rank3_baths"],
                               Rank3_size=variables["Rank3_size"],
                               Rank3_address=variables["Rank3_address"],
                               Rank3_School=variables["Rank3_School"],
                               Rank3_Metro=variables["Rank3_Metro"],
                               Rank3_BusStop=variables["Rank3_BusStop"],
                               Rank3_CommunityCenter=variables["Rank3_CommunityCenter"],
                               Rank3_Library=variables["Rank3_Library"],
                               Rank3_Restaurant=variables["Rank3_Restaurant"],
                               Rank3_Bars=variables["Rank3_Bars"],
                               Rank3_MoreRestaurants=variables["Rank3_MoreRestaurants"],
                               Rank3_MoreBars=variables["Rank3_MoreBars"],
                               Rank3_Agent_name=variables["Rank3_agent_name"],
                               Rank3_phnumber=variables["Rank3_phnumber"],
                               # Rank 4
                               Rank4_thumbnail=variables["Rank4_thumbnail"],
                               Rank4_Price=variables["Rank4_Price"],
                               Rank4_beds=variables["Rank4_beds"],
                               Rank4_baths=variables["Rank4_baths"],
                               Rank4_size=variables["Rank4_size"],
                               Rank4_address=variables["Rank4_address"],
                               Rank4_School=variables["Rank4_School"],
                               Rank4_Metro=variables["Rank4_Metro"],
                               Rank4_BusStop=variables["Rank4_BusStop"],
                               Rank4_CommunityCenter=variables["Rank4_CommunityCenter"],
                               Rank4_Library=variables["Rank4_Library"],
                               Rank4_Restaurant=variables["Rank4_Restaurant"],
                               Rank4_Bars=variables["Rank4_Bars"],
                               Rank4_MoreRestaurants=variables["Rank4_MoreRestaurants"],
                               Rank4_MoreBars=variables["Rank4_MoreBars"],
                               Rank4_Agent_name=variables["Rank4_agent_name"],
                               Rank4_phnumber=variables["Rank4_phnumber"],
                               # Rank 5
                               Rank5_thumbnail=variables["Rank5_thumbnail"],
                               Rank5_Price=variables["Rank5_Price"],
                               Rank5_beds=variables["Rank5_beds"],
                               Rank5_baths=variables["Rank5_baths"],
                               Rank5_size=variables["Rank5_size"],
                               Rank5_address=variables["Rank5_address"],
                               Rank5_School=variables["Rank5_School"],
                               Rank5_Metro=variables["Rank5_Metro"],
                               Rank5_BusStop=variables["Rank5_BusStop"],
                               Rank5_CommunityCenter=variables["Rank5_CommunityCenter"],
                               Rank5_Library=variables["Rank5_Library"],
                               Rank5_Restaurant=variables["Rank5_Restaurant"],
                               Rank5_Bars=variables["Rank5_Bars"],
                               Rank5_MoreRestaurants=variables["Rank5_MoreRestaurants"],
                               Rank5_MoreBars=variables["Rank5_MoreBars"],
                               Rank5_Agent_name=variables["Rank5_agent_name"],
                               Rank5_phnumber=variables["Rank5_phnumber"],
                               # Rank 6
                               Rank6_thumbnail=variables["Rank6_thumbnail"],
                               Rank6_Price=variables["Rank6_Price"],
                               Rank6_beds=variables["Rank6_beds"],
                               Rank6_baths=variables["Rank6_baths"],
                               Rank6_size=variables["Rank6_size"],
                               Rank6_address=variables["Rank6_address"],
                               Rank6_School=variables["Rank6_School"],
                               Rank6_Metro=variables["Rank6_Metro"],
                               Rank6_BusStop=variables["Rank6_BusStop"],
                               Rank6_CommunityCenter=variables["Rank6_CommunityCenter"],
                               Rank6_Library=variables["Rank6_Library"],
                               Rank6_Restaurant=variables["Rank6_Restaurant"],
                               Rank6_Bars=variables["Rank6_Bars"],
                               Rank6_MoreRestaurants=variables["Rank6_MoreRestaurants"],
                               Rank6_MoreBars=variables["Rank6_MoreBars"],
                               Rank6_Agent_name=variables["Rank6_agent_name"],
                               Rank6_phnumber=variables["Rank6_phnumber"],
                               )


@app.route('/',methods=['GET', 'POST'])  # HomePage Url - Shows the user the questionnare
def redirect():
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
