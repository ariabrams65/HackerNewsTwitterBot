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
    posts = get_posts()
    with PostDatabase('posts.db') as db:
        for post in posts:
            if not db.has_post(post['id']):
                db.add_post(post['id'])
                return post
            

def get_text_to_tweet(post):
    text = f'{post["title"]}: '
    if (post['source'] is not None):
        text += f'{post["link"]}\n'
    text += f'\nComments: {post["comments_link"]}'
    return text


def send_tweet(text):
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    response = client.create_tweet(text=text)


if __name__ == '__main__':
    post = get_new_post()
    if post is not None:
        tweet = get_text_to_tweet(post)
        send_tweet(tweet)
