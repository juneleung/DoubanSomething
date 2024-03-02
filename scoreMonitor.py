from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import os, json


def getData(page,id):
    page.goto('https://movie.douban.com/subject/'+id+'/')
    
    # 分数
    rating = page.query_selector('.rating_num').text_content()

    # 人数
    rating_sum = page.wait_for_selector('div.rating_sum')
    text_content = rating_sum.text_content()
    people_count = text_content.split('人评价')[0].strip()

    # 分层星比
    items = page.query_selector_all('.ratings-on-weight .item')
    ratings = {}
    percentageAll = ""
    for item in items:
        stars = item.query_selector('span.starstop').inner_text()
        rating_per = item.query_selector('span.rating_per').inner_text()
        ratings[stars] = rating_per
    for star, percentage in ratings.items():
        # print(f"{star}: {percentage}")
        percentageAll = percentageAll + "/" +percentage
    movie_ratings = {
                "rate": rating,
                "people_count": people_count,
                "percentage": percentageAll,
            }
    # print(movie_ratings)
    return movie_ratings

def check_dune_rating():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        dune1 = getData(page,"3001114")#dune1
        dune2 = getData(page,"35575567")#dune2
        oppen = getData(page,"35593344")#oppen
        browser.close()

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open('dune_ratings.txt', 'a+', encoding='utf-8') as file:
            file.write(json.dumps(dune1) + '\t')
            file.write(json.dumps(dune2) + '\t')
            file.write(json.dumps(oppen) + '\n')

def write_to_file(data):
    with open('dune_ratings.txt', 'a', encoding='utf-8') as file:
        file.write(data + '\n')

import time

while True:
    check_dune_rating()
    # time.sleep(60) #1min
    time.sleep(3600) #1hr