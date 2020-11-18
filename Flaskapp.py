"""  This file creates the Flask application reuired to render the Webpage and display the final Listing to user """

from flask import Flask, request, jsonify, render_template, redirect
from Filter_Listings import PropertyFilter

# from Attribute Hierarchy Model - Proof of Concept.py import the user defined function


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
    print(PropertyFilter(session_data))
    return render_template('Real_Estate_Listings_Dynamic_Final.html',
                           Property_Type=session_data['propertyTypeName'],
                           Bedroom_Filter=session_data["bedroom"],
                           Bathroom_Filter=session_data['bathroom'],
                           Travel_Mode=session_data['distance'])
    # Rank6_thumbnail="https://ap.rdcpix.com/b1d084dc0c94bef6efd272796a63d907l-m3038600760x.jpg",
    # Rank6_Price="$270,000")


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
