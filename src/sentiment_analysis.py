'''
Performs sentiment analysis on Reddit comments related to the hot topics fetched.
Stores processed results in a csv file.
'''

import pandas as pd
from transformers import pipeline
from gather_data import get_city_data

def s_a(city_name):

    sentiment_pipeline = pipeline('sentiment-analysis')
    result_data = get_city_data(city_name)
    if result_data is None:
        print(f"No data retrieved for {city_name}. Exiting.")
        return

    sentiment_df = pd.DataFrame(columns=['comment_sentiment', 'comment_sentiment_score'])
    city_df = pd.DataFrame(columns=['headline', 'post_title', 'comment_body'])

    for headline, topics in result_data.items():
        for topic in topics:
            for comment in topic['comments']:
                comment_text = comment['body']
                comment_sentiment = sentiment_pipeline(comment_text[:512])[0]
                
                sentiment_df = sentiment_df._append({
                    'comment_sentiment': comment_sentiment['label'],
                    'comment_sentiment_score': comment_sentiment['score'],
                }, ignore_index=True)

                city_df = city_df._append({
                    'headline': headline,
                    'post_title': topic['title'],
                    'comment_body': comment_text,
                }, ignore_index=True)

    city_df = pd.concat([city_df, sentiment_df], axis=1)
    # csv_filename = f'data/{city_name}_sentiment_analysis.csv'
    # city_df.to_csv(csv_filename, index=False)

    print('Sentiment Analysis completed')

    return city_df

# Test function - 1
# city_name = input('Enter city name: ')
# sentiment_df = s_a(city_name)