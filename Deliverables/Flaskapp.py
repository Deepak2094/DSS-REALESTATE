"""  This file creates the Flask application reuired to render the Webpage and display the final Listing to user """

from flask import Flask, request, jsonify, render_template, redirect
from Filter_Listings import PropertyFilter
from Model import create_ranked_data
import pandas

app = Flask(__name__)

session_data = {}


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
    print(session_data)
    if PropertyFilter(session_data) == "There are no listings that fit your criteria":
        return render_template("DSS_Redirected.html")
    else:
        create_ranked_data(PropertyFilter(session_data), Environmental_Features)
        return render_template('Real_Estate_Listings_Dynamic_Final.html',
                               Property_Type=session_data['propertyTypeName'],
                               Bedroom_Filter=session_data["bedroom"],
                               Bathroom_Filter=session_data['bathroom'],
                               Travel_Mode=session_data['distance'],
                               housePrice=session_data['housePriceName'])


# Rank1_Price
# Rank1_beds
# Rank1_baths
# Rank1_size
# Rank1_address
# Rank1_School
# Rank1_Metro
# Rank1_BusStop
# Rank1_CommunityCenter
# Rank1_Library
# Rank1_Restaurant
# Rank1_Bars

# @app.route("/youwereredirected")
# def redirected():
#     return render_template('DSS_Redirected.HTML')
#     # return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

# Reference
# return render_template('DSS_Form_Page_2.HTML', variable=variable)
#  variable = Page1["bedroom"]
#     print(Page1)
#     return render_template('DSS_Form_Page_2.HTML', variable=variable)
#     Listings = "None"
# if Listings == "None":
#     return redirect('/youwereredirected')
# else:
