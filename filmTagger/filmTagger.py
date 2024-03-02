from playwright.sync_api import Playwright, sync_playwright, expect
import json, os

# -----------------------------
tagTo = "wish" #想看
# tagTo = "collect" #看过
# tagTo = "do" #在看
# -----------------------------


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
    if(not os.path.exists(loginInfo)):
        login(playwright,loginInfo)

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(storage_state=loginInfo)
    page = context.new_page()
 
    page.goto("https://movie.douban.com/mine?status="+tagTo)
    pageNum = 1
    # userID = ""
    # page.goto("https://movie.douban.com/people/"+str(userID)+"/wish?start="+str(30*(pageNum-1))+"&sort=time&rating=all&filter=all") #想看
    # page.goto("https://movie.douban.com/people/"+str(userID)+"/collect?start="+str(30*(pageNum-1))+"&sort=time&rating=all&filter=all") #看过
    lilist = page.query_selector_all('li.list')
    if lilist:
        lilist[0].click()
    else:
        print("Error: 无法打开列表")
        exit(0)

    while pageNum:
        items = page.query_selector_all('.list-view .item')
        for item in items:
            print("-"*50)
            # film lists
            title = item.query_selector('.title a')
            title_text = title.inner_text()
            link = title.get_attribute('href')
            print(f"***: p{pageNum} {title_text} {link}")
            if title_text == "未知电影": 
                print("Error: 未知电影, 跳过")
                continue

            sub_page = browser.new_page(storage_state=loginInfo)
            sub_page.goto(link)

            html_content = sub_page.inner_html('html')
            if "你想访问的页面不存在" in html_content or  "没有权限" in html_content:
                print("Error: 页面不存在/没有权限")
                continue
            if ">修改</a>" not in html_content:
                print("Error: 不让修改, dddd")
                continue

            title, keywords = getFilmTags(sub_page)
            print(" ".join(keywords))

            # 修改标签
            sub_page.get_by_role("link", name="修改").first.click()
            sub_page.locator("input[name=\"tags\"]").click()
            sub_page.locator("input[name=\"tags\"]").press("Meta+a")
            sub_page.locator("input[name=\"tags\"]").fill(" ".join(keywords))
            sub_page.get_by_role("button", name="保存").click() 

            sub_page.close()
        
        link_element = page.query_selector('a:has-text("后页>")')
        has_link = bool(link_element)
        if has_link:
            pageNum = pageNum + 1
            print(pageNum)
            page.get_by_role("link", name="后页>").click()
        else:
            break

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
