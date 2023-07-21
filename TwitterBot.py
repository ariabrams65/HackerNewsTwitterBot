import tweepy
import os
from dotenv import load_dotenv
from HackerNewsScraper import get_posts
from db import PostDatabase

load_dotenv()
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

def get_new_post():
    posts = get_posts(min_points=100)
    with PostDatabase('posts.db') as db:
        for post in posts:
            if not db.has_post(post['id']):
                db.add_post(post['id'])
                return post


def send_tweet(text):
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    response = client.create_tweet(text=text)


if __name__ == '__main__':

    post = get_new_post()
    send_tweet('test3')
