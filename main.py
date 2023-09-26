#!/usr/local/bin/python3
import rssparser  # 보안뉴스
import xmlparser  # google
import naverparser  # naver
import makepage
from datetime import datetime
from datetime import timedelta
from datetime import timezone

content = []  # 담겨질 컨텐츠

xmllink = [
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/563367945796465169",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/5100263147140437623",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/13994762689153573568",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/13979299383437263462",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/13979299383437266274",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/1643862750533404189",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/16645802662687679867",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/12473829239092869905",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/2796372246252066736",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/15841228778190866138",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/5654189484818916956",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/10931067280370148204",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/7028492564145325603",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/7028492564145327494",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/7028492564145324676",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/7028492564145327245",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/7028492564145327576",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/7028492564145325204",
    "https://www.google.co.kr/alerts/feeds/07823680028175865471/5552825568548004949",
]

rsslink = [
    "http://www.boannews.com/media/news_rss.xml",
    "https://www.dailysecu.com/rss/allArticle.xml",
]

## 네이버 추가
keywords = [
    "정보보안",
    "정보보호",
    "개인정보",
    "해킹",
    "유출",
    "클라우드",
    "랜섬웨어",
    "취약점",
    "블록체인 보안",
    "메타버스 보안",
    "NFT 보안",
    "블록체인 해킹",
    "암호화폐 유출",
    "블록체인 유출",
    "암호화폐 해킹",
    "NFT 해킹",
]


for link in rsslink:
    rsscontent = rssparser.getFeed(link)
    content.extend(rsscontent)

for link in xmllink:
    xmlcontent = xmlparser.getContent(link)
    content.extend(xmlcontent)

## 네이버 추가
for keyword in keywords:
    navercontent = naverparser.getContentFromNaver(keyword)
    content.extend(navercontent)

## 중복 컨텐츠 삭제
bucket = set()
publish_content = []
today = datetime.now()
for c in content:
    if c["link"] not in bucket:
        bucket.add(c["link"])
        ## 오늘 날짜 필터링 <임시>
        if isinstance(c["date"], str):
            news_date = datetime.strptime(c["date"], "%Y-%m-%d %H:%M:%S")
            if today - news_date < timedelta(days=2):
                publish_content.append(c)
        elif isinstance(c["date"], datetime):
            if today - c["date"].replace(tzinfo=None) < timedelta(days=2):
                publish_content.append(c)
makepage.make_page(publish_content, content_length=150)
# with open('news.txt','w') as f:
#    for c in content:
#        news = "{}||{}\n".format(c['title'],c['link'])
#        f.write(news)
