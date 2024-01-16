'''
Authenticating with the Reddit API using praw and script authentication. 
Utility functions for retrieving and storing city-related data from Reddit.

- "authenticate_reddit_script" - Authenticates Reddit API for data retrieval.
- "get_city_data(city)" - Retrieves data from Reddit for a given city based on top headlines.
- "create_database(city_data, db_path='data/city_db.db')" - Creates and populates an SQLite database with the retrieved data.
'''

import praw
import json
import sqlite3
import os
from fetch_headlines import fetch_top_news

def authenticate_reddit_script():
    try:
        with open('keys/details.json', 'r') as config_file:
            credentials = json.load(config_file)['reddit']
    except FileNotFoundError:
        print("Error: keys/details.json file not found.")
        return None
    except KeyError:
        print("Error: Invalid or missing 'reddit' section in keys/details.json.")
        return None

    reddit = praw.Reddit(
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        username=credentials['username'],
        password=credentials['password'],
        user_agent='MyRedditApp/1.0',
    )

    return reddit

def get_city_data(city):

    headlines = fetch_top_news(city)
    if not headlines:
        print(f"No headlines found for {city}. Exiting.")
        return None

    reddit_instance = authenticate_reddit_script()
    if not reddit_instance:
        print("Reddit authentication failed. Exiting.")
        return None

    city_data = {}
    print(headlines, '\n', '\n')
    for headline in headlines:
        discussions = reddit_instance.subreddit('all').search(headline, sort='relevance', time_filter='month', limit=5)

        topic_data = []
        for submission in discussions:
            submission_data = {
                "title": submission.title,
                "url": submission.url,
                "score": submission.score,
                "comments": []
            }

            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list()[:10]:
                submission_data["comments"].append({
                    "body": comment.body,
                    "score": comment.score
                })

            topic_data.append(submission_data)

        city_data[headline] = topic_data

    return city_data

# def create_database(city_data, city_name):
#     db_path = f'data/{city_name}.db'
#     try:
#         os.makedirs(os.path.dirname(db_path), exist_ok=True)
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()

#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS headlines (
#                 id INTEGER PRIMARY KEY,
#                 city TEXT,
#                 headline TEXT
#             )
#         ''')

#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS posts (
#                 id INTEGER PRIMARY KEY,
#                 headline_id INTEGER,
#                 title TEXT,
#                 url TEXT,
#                 score INTEGER,
#                 FOREIGN KEY (headline_id) REFERENCES headlines(id)
#             )
#         ''')

#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS comments (
#                 id INTEGER PRIMARY KEY,
#                 post_id INTEGER,
#                 body TEXT,
#                 score INTEGER,
#                 FOREIGN KEY (post_id) REFERENCES posts(id)
#             )
#         ''')

#         for headline, topics in city_data.items():
#             cursor.execute('INSERT INTO headlines (city, headline) VALUES (?, ?)', (city_name, headline))
#             headline_id = cursor.lastrowid

#             for topic in topics:
#                 cursor.execute('INSERT INTO posts (headline_id, title, url, score) VALUES (?, ?, ?, ?)',
#                                (headline_id, topic['title'], topic['url'], topic['score']))
#                 post_id = cursor.lastrowid

#                 for comment in topic['comments']:
#                     cursor.execute('INSERT INTO comments (post_id, body, score) VALUES (?, ?, ?)',
#                                    (post_id, comment['body'], comment['score']))
#         conn.commit()
#         conn.close()

#         print("Data successfully stored in the database.")

#     except Exception as e:
#         print(f"Error creating database: {e}")

#Test function - 1
# reddit_instance = authenticate_reddit_script()
# if reddit_instance:
#     print('Script authentication works')
#     print(f"Authenticated as: {reddit_instance.user.me().name}")

#Test function - 2
# city_name = input("Enter city name: ")
# result_data = get_city_data(city_name)
# if result_data:
#     print(f"Data for {city_name}:\n{result_data}")

#Test function - 3
# city_name = input("Enter city name: ")
# result_data = get_city_data(city_name)
# if result_data:
#     create_database(result_data, city_name)