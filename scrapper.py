import requests
from bs4 import BeautifulSoup
import pprint
import sys

try:
    pages = int(sys.argv[1])
except:
    print(
        f'\n The first argument needs to be an integer value of 1 or bigger! The program will exit now! \n')


def collect_raw_data(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


for page in range(1, pages+1):
    print(f'Page {page}: \n')
    raw_data = collect_raw_data(f'https://news.ycombinator.com/news?p={page}')
    links = raw_data.select('.storylink')
    subtext = raw_data.select('.subtext')

    pprint.pprint(create_custom_hn(links, subtext))
