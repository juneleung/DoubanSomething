from playwright.sync_api import Playwright, sync_playwright, expect
import json, os



def getFilmTags(sub_page):
    keywords = []

    year = sub_page.query_selector('.year').inner_text().strip().replace("(","").replace(")","")
    # print(f"年份: {year}")
    keywords.append(year) if year else None

    # 获取电影标题
    title_element = sub_page.query_selector('#content > h1 > span[property="v:itemreviewed"]')
    title = title_element.inner_text()
    # print(f"电影标题: {title}")
    # keywords.append(title) if title else None

    # 导演
    director_elements = sub_page.query_selector_all('#info span.pl:has-text("导演") + span.attrs a')
    if director_elements:
        for director_element in director_elements:
            director = director_element.inner_text()
            # print(f"导演: {director}")
            if director is not None:
                keywords += director.replace(" ","_").split(" / ")
    
    # 类型
    genre_elements = sub_page.query_selector_all('#info span[property="v:genre"]')
    if genre_elements:
        for genre_element in genre_elements:
            genre = genre_element.inner_text()
            if genre is not None:
                # print(f"类型: {genre}")
                keywords += genre.split(" / ")

    # 制片国家
    language_label_span = sub_page.query_selector('#info span.pl:has-text("制片国家/地区")')
    if language_label_span:
        language = sub_page.evaluate('(element) => element.nextSibling.nodeValue', language_label_span)
        if language is not None:
            # print(f"制片国家/地区: {language}")
            keywords += language.split(" / ")

    # 当前分数
    rating = sub_page.query_selector('.ll.rating_num[property="v:average"]')
    # print(f"当前分数: {rating}")
    if rating:
        rating = rating.inner_text()
        if rating:
            rating = str(int(float(rating))) + "分"
            keywords.append(rating)

    return title, keywords

def login(playwright,loginInfo):
    # login
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://accounts.douban.com/passport/login?source=movie")
    page.locator(".quick").first.click()

    page.wait_for_url("https://www.douban.com/")
    
    storage_state = page.context.storage_state()
    
    f = open(loginInfo, 'w')
    json.dump(storage_state, f)
    f.close()

    page.close()
    browser.close()

loginInfo = "loginInfo.json"
def run(playwright: Playwright) -> None:
    # if(not os.path.exists(loginInfo)):
    #     login(playwright,loginInfo)

    browser = playwright.chromium.launch(headless=True)
    # context = browser.new_context(storage_state=loginInfo)
    context = browser.new_context()
    page = context.new_page()
 
    page.goto("https://movie.douban.com/top250")
    pageNum = 1
    page.wait_for_selector("ol > li")

    while pageNum:
        items = page.query_selector_all("ol > li")

        for item in items:
            title = item.query_selector(".info > .hd > a > span.title").inner_text()
            link = item.query_selector(".info > .hd > a").get_attribute("href")

            # print("-"*50)
            # print(title,link)
            print(title)
        
        link_element = page.query_selector('a:has-text("后页>")')
        has_link = bool(link_element)
        if has_link:
            pageNum = pageNum + 1
            # print(pageNum)
            page.get_by_role("link", name="后页>").click()
        else:
            break

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)