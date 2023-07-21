import requests
from bs4 import BeautifulSoup
import re
import json
import time

def get_post(athing, subline, url):
    post = {}
    pattern = re.compile(r'\d+')
    titleline = athing.find(class_='titleline')
    sitestr_element  = titleline.find(class_='sitestr')
    comments = subline.contents[-2]
    title = titleline.find('a', class_=False)

    post['title'] = str(title.string)
    post['link'] = title['href']
    post['source'] = None if not sitestr_element else str(sitestr_element.string)
    post['id'] = athing['id']
    post['points'] = pattern.match(str(subline.find(class_='score').string)).group()
    post['time'] = subline.find(class_='age')['title']
    post['comments_link'] = url + comments['href']
    post['num_comments'] = '0' if comments.string == 'discuss' else pattern.match(str(comments.string)).group()

    return post


def get_soup(url, contentType, page_num):
    response = requests.get(url + f'{contentType}?p={page_num}')
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_posts(contentType='news', min_points=0):
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
    
    filtered_posts = [post for post in posts if int(post['points']) >= min_points] 
    return sorted(filtered_posts, key=lambda post : post['points'], reverse=True)


if __name__ == '__main__':
    posts = get_posts(min_points=100)
    print(json.dumps(posts, indent=4))