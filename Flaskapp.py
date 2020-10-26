"""  This file creates the Flask application reuired to render the Webpage and display the final Listing to user """

from flask import Flask, request, jsonify, render_template, redirect

# from Attribute Hierarchy Model - Proof of Concept.py import the user defined function


app = Flask(__name__)


@app.route('/')  # HomePage Url - Shows the user the questionnare
def home_page():
    return render_template('DSS_Form.HTML')


@app.route('/DSS_RealEstate', methods=["post"])  # This Url recieves the input from the user
def DSS_RealEstate():
    print(request.form)
    data = request.form.to_dict()
    variable = data["bedroom"]
    print(data)
    # Listings = "None"
    # if Listings == "None":
    #     return redirect('/youwereredirected')
    # else:
    return render_template('Real_Estate_Listings_static.html', variable=variable)


# @app.route("/youwereredirected")
# def redirected():
#     # return render_template('DSS_Redirected.HTML')
#     return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
