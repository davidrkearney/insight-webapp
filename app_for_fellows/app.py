from flask import Flask, render_template, request
import requests
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import StandardScaler
pd.options.display.max_columns=25


#This is the function that outputs recommendations for my app. You'll replace this with your function that takes in the user input and gives the output
def cos_sim_recommendations(new_data, df, index_name, n=1):
    cs = cosine_similarity(new_data, df)
    rec_index = np.argsort(cs)[0][-n-1:][::-1][1:]
    recommendations = []
    for rec in rec_index:
        recommendations.append(index_name[rec])
    return recommendations

#Initialize app
app = Flask(__name__, static_url_path='/static')

#Standard home page. 'index.html' is the file in your templates that has the CSS and HTML for your app
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#My home page redirects to recommender.html where the user fills out a survey (user input)
@app.route('/recommender', methods=['GET', 'POST'])
def recommender():
    return render_template('recommender.html')

#After they submit the survey, the recommender page redirects to recommendations.html
@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    vendors = pd.read_csv('data/florists_updated.csv')

    ### bunch of data cleaning functions

    # standardize my features
    X = vendors[features].values
    ss = StandardScaler()
    X = ss.fit_transform(X)

    # These are a couple examples of what the user input looks like.

    #1. user enters the total price of the wedding. The name of the variable is arbitrary and doesn't have to be the same but is less confusing later on
    total_price = float(request.form['total_price'])

    #2. user also enters size of wedding
    size_of_wedding = int(request.form['size_of_wedding'])

    ### other user inputs


    new_df = pd.DataFrame({
                        'total_price':total_price,
                        'size_of_wedding':size_of_wedding,
                        #etc....
                        })
    #call the recommender function
    cos_sims = cos_sim_recommendations(new_df, X, index_name, n=1)

    #for my app the recommender gives an image of the florist and a link
    florist_info = {
    'Flora_by_Nora':
        {'name':'Flora by Nora', 'img_src':'/static/img/flora_by_nora.png', 'link':'https://www.florabynora.com/'},
    'Madelyn_Claire_Floral_Design_&_Events':
        {'name':'Madlyn Claire Floral Design', 'img_src':'/static/img/madelyn_claire.png', 'link':'https://madelynclairefloraldesign.com/'},
    'Little_Shop_of_Floral':
        {'name':'Little Shop of Floral', 'img_src':'/static/img/little_shop_of_floral.png', 'link':'https://www.littleshopoffloral.com/'},
    'Lumme_Creations':
        {'name':'Lumme Creations', 'img_src':'/static/img/lumme.png', 'link':'https://www.lummecreations.com/'},
    'Rooted':
        {'name':'Rooted Floral and Design', 'img_src':'/static/img/rooted.png', 'link':'https://www.rootedfloralanddesign.com/'},
    'Blush_&_Bay':
        {'name':'Blush and Bay', 'img_src':'/static/img/blush_and_bay.png', 'link':'http://www.blushandbay.com/'}}


    #arguments are whatever comes out of your app, in my case a cos_sim and the recommended florist
    #the structure is render_template('your_html_file.html', x=x, y=y, etc...)
    #refer to my recommendations.html to see how variables work
    return render_template('recommendations.html', cos_sims = cos_sims, florist_info = florist_info)


if __name__ == '__main__':
    #this runs your app locally
    app.run(host='0.0.0.0', port=8080, debug=True)
