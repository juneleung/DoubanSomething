# -*- coding: utf-8 -*-
from __future__ import print_function
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import re

filmlist = ["超人王朝","正义联盟大战致命五人组","王者少年","玻璃先生","驯龙高手3","乐高大电影2","冷血追击","惊奇队长","我们","宠物坟场","小飞象","狼嚎","雷霆沙赞！","阿丽塔：战斗天使","不可能的事","地狱男爵：血皇后崛起","复仇者联盟4：终局之战","大侦探皮卡丘","蝙蝠侠：缄默","火箭人","哥斯拉2：怪兽之王","爱宠大机密2","疾速追杀3","蝙蝠侠大战忍者神龟","阿拉丁","魔童","黑衣人：全球追缉","X战警：黑凤凰","优步危机","夏福特","安娜","昨日奇迹","狮子王","玩具总动员4","神奇女侠：血脉","蜘蛛侠：英雄远征","超人之死与超人归来","在黑暗中讲述的恐怖故事","速度与激情：特别行动","仲夏夜惊魂","天使陷落","好莱坞往事","小丑回魂2","舞女大盗","阿波罗11号","七个世界，一个星球","星际探索","第一滴血5：最后的血","雪人奇缘","小丑","沉睡魔咒2","丧尸乐园2","双子杀手","乔乔的异想世界","冰雪奇缘2","小羊肖恩2：末日农场","扫毒2.：天地对决","极速车王","睡梦医生","终结者：黑暗命运","邻里美好的一天","多力特的奇幻冒险","史酷比狗","超人：明日之子","格蕾特和韩塞尔","花木兰","釜山行2：半岛","骨肉","混沌行走","速度与激情9","电锯惊魂9：漩涡","特种空勤团：红色通缉令","怪物猎人","太空异旅","真人快打","007系列25：无暇赴死","760号犯人","毒液2","警醒","哭泣的男人","平安夜","沙丘","糖果人","天赐灵机","原钻","最后的决斗","355：谍影特攻","Soho区惊魂夜","冰路营救","北海","唐顿庄园","圣母","埃菲尔铁塔","尼罗河上的惨案","怒火·重案","惊声尖叫5","月光光心慌慌：杀戮","欢乐好声音2","永恒族","猫女：猎捕","玉面情魔","王牌特工：源起","纽瓦克众圣","美国草根：库尔特·华纳的故事","致命女郎","致埃文·汉森","蜘蛛侠：英雄无归","警察局","超能敢死队","魔法满屋","黑客帝国：矩阵重启","无限","奇迹·笨小孩","青春变形记","神奇动物：邓布利多之谜","冰冻星球 第二季","唐顿庄园2","老亨利","侏罗纪世界3","神秘海域","月球陨落","绿色星球","燃烧的巴黎圣母院","黄石镇谋杀案","记忆","奇异博士2：疯狂多元宇宙","羊崽","犬之力","DC萌宠特遣队","X","安妮特","暗夜博士：莫比亚斯","巴布与斯塔尔的维斯塔德尔玛之旅","北欧人","蝙蝠侠：漫长的万圣节(上)","蝙蝠侠和超人：超凡双子之战","不","承包商","刺猬索尼克2","光年正传","国王理查德","黑匣子","坏蛋联盟","健听女孩","开心汉堡店","哭悲","雷神4：爱与雷霆","猫王","迷失之城","男人","清道夫：布局","雀斑公主","人之怒","瞬息全宇宙","套装","天才不能承受之重","亡命救护车","未来罪行","小黄人大眼萌：神偷奶爸前传","新蝙蝠侠","亚当斯一家2","真人快打传奇：雪盲","致命感应","壮志凌云2：独行侠","子弹列车","三千年的渴望","亲爱的别担心","北区侦缉队","危笑","忌日快乐2","达荷美女战士","阿姆斯特丹","鳄鱼莱莱"]

targetUrls = []
driver = webdriver.Chrome()

def get_data(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363'}
    resp = requests.get(url=url, headers=header)
    if resp.status_code == 200:
        page = BeautifulSoup(resp.text,'html.parser')

        # title
        title = page.find_all(id = 'content' )
        set_title = re.compile('property="v:itemreviewed">(.*?)</span>')
        title = re.findall(set_title,str(title))

        # year
        year = page.find_all(class_ = 'year')
        year = re.findall(">(.*?)</span>",str(year))

        # imdb
        rate = page.find_all(class_ = 'pl')
        imdb = re.findall('IMDb:</span> (.*)<br/>',str(page))

        return title,imdb,year
        # return resp.text
    else:
        print('status_code: ', resp.status_code)
        return ''

for filmname in filmlist:
    url = "https://movie.douban.com/subject_search?search_text=" + filmname
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    soup1 = BeautifulSoup(html, 'lxml')
    if len(soup1.select('a.title-text'))>0:
        targetUrl = soup1.select('a.title-text')[0].get('href')
        title,imdb,year = get_data(targetUrl)
        if(len(title)):
            print(f"{title[0]}\t{year[0]}\t{imdb[0]}\t{targetUrl}")
        else:
            print(f"not found douban page of {filmname}")
        targetUrls.append(targetUrl)
    else:
        targetUrl = "no result"
        print(targetUrl)
        targetUrls.append(targetUrl)

driver.close()