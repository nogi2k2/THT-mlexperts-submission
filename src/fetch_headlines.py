'''
Keyword based search, api retrieves top news listing for the keyword. Keyword in this case is the city name.
'''

import requests
import json

def fetch_top_news(city):
    try:
        with open('keys/details.json', 'r') as json_file:
            keys = json.load(json_file)
            api_key = keys.get('news_api', {}).get('api_key', '')
    except FileNotFoundError:
        print("Error: keys/details.json file not found.")
        return []

    if not api_key:
        print("Error: News API key not found in keys/details.json.")
        return []

    url = f'https://newsapi.org/v2/everything?q={city}&sortBy=popularity&apiKey={api_key}&pageSize=5'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        headlines = []

        for post in data['articles'][:5]:
            title = post['title']
            published_at = post['publishedAt']
            headlines.append(f"{title} - {published_at}")

        return headlines

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


# city_name = 'Agra'
# news_headlines = fetch_top_news(city_name)
# if news_headlines:
#     print(f"Top 5 headlines in {city_name}:")
#     for i, headline in enumerate(news_headlines, 1):
#         print(f"{i}. {headline}")