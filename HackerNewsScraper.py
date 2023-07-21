import requests
from bs4 import BeautifulSoup
import re
import json
import time

def get_post(athing, subline, url):
    post = {}
    titleline = athing.find(class_='titleline')
    title = titleline.find('a', class_=False)
    post['title'] = title.string
    post['link'] = title['href']
    sitestr_element  = titleline.find(class_='sitestr')
    post['source'] = None if not sitestr_element else sitestr_element.string
    post['id'] = athing['id']
    post['points'] = subline.find(class_='score').string
    post['time'] = subline.find(class_='age')['title']
    comments = subline.contents[-2]
    post['comments_link'] = url + comments['href']
    post['num_comments'] = '0' if comments.string == 'discuss' else re.compile(r'\d+').match(comments.string).group()

    return post


def get_soup(url, contentType, page_num):
    response = requests.get(url + f'{contentType}?p={page_num}')
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_posts(contentType='news'):
    url = 'https://news.ycombinator.com/'
    posts = []
    page_num = 1
    while True:
        soup = get_soup(url, contentType, page_num)
        if not soup.find(class_='athing'):
            break

        athings = soup.find_all(class_='athing') 
        sublines = soup.find_all(class_='subline')
        for athing, subline in zip(athings, sublines):
            posts.append(get_post(athing, subline, url))
        
        page_num += 1
        time.sleep(1)
    
    return posts


if __name__ == '__main__':
    posts = get_posts()