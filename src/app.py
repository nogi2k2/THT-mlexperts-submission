from flask import Flask, render_template, request
from sentiment_analysis import s_a
import pandas as pd

app = Flask(__name__)

api_options = ['news api']
website_options = ['reddit']

@app.route('/', methods=['GET', 'POST'])
def index():

    sentiment_stats_dict = {} 

    if request.method == 'POST':
        city_name = request.form['city']
        selected_api = request.form['api']
        selected_website = request.form['website']

        result_df = s_a(city_name)
        sentiment_stats_dict = process_sentiment_statistics(result_df)

    return render_template('index.html', sentiment_stats_dict=sentiment_stats_dict, api_options=api_options, website_options=website_options)

def process_sentiment_statistics(df):
    sentiment_stats = df.groupby(['headline', 'comment_sentiment']).size().unstack(fill_value=0)

    sentiment_stats_dict = {
        'headlines': list(sentiment_stats.index),
        'positive_comments': list(sentiment_stats['POSITIVE']),
        'negative_comments': list(sentiment_stats['NEGATIVE']),
    }

    return sentiment_stats_dict

if __name__ == '__main__':
    app.run(debug=True)

