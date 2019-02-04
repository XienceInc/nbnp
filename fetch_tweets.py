import json, access_token
from requests_oauthlib import OAuth1Session

def accumulate_data():
    ck = access_token.CONSUMER_KEY
    cs = access_token.CONSUMER_SECRET
    at = access_token.ACCESS_TOKEN
    ats = access_token.ACCESS_TOKEN_SECRET

    # url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    # params = {'count': 10}

    positive_tweet_ids = [
        1067776702879686656,
        1091726297124896768,
        1092202678619332608,
        1091707040106336256,
        1092185956696809473,
        1092039095042207744,
        1090238950336212992,
        ]
    negative_tweet_ids = [
        1092214371139219457,
        1092182541933588480,
        1092040673165885442,
        1092070238164738048,
        1092216819409027072,
        1091255883009413123,
        1092230511190134784,
        1088377968596897792,
        1061663912989417472,
    ]

    positive_tweets = []
    negative_tweets = []

    twitter = OAuth1Session(ck, cs, at, ats)

    # accumulate positive tweets
    for tweet_id in positive_tweet_ids:
        tweet_text = fetch_tweet_text(twitter, tweet_id)
        if tweet_text is None:
            continue
        positive_tweets.append(tweet_text)
        
    # accumulate negative tweets
    for tweet_id in negative_tweet_ids:
        tweet_text = fetch_tweet_text(twitter, tweet_id)
        if tweet_text is None:
            continue
        negative_tweets.append(tweet_text)

    return positive_tweets, negative_tweets

def fetch_tweet_text(twitter_session, tweet_id):
    url = 'https://api.twitter.com/1.1/statuses/show.json'
    params = {'id': tweet_id, 'trim_user': 1}
    res = twitter_session.get(url, params=params)
    if res.status_code != 200:
        print("Error code:", res.status_code)
        return None
    json_data = json.loads(res.text)
    return json_data['text']

if __name__ == '__main__':
    pos, nega = accumulate_data()

    print('------- Positive tweets -------')
    for text in pos:
        print(text, '\n')
    print('\n------- Negative tweets -------')
    for text in nega:
        print(text, '\n')
