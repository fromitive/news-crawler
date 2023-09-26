import feedparser
import time
from xmlparser import getDetail


def getFeed(url):
    feed = feedparser.parse(url)
    result = []
    for entry in feed.entries:
        item = {"title": "", "date": "", "link": "", "detail": None}
        t = entry.get("updated_parsed")
        published = time.strftime("%Y-%m-%d %H:%M:%S", t)
        print("published:\t", published)
        print("title\t", entry.get("title", ""))
        # print("link:\t",entry.get("link", ""))
        # print("description:")
        # print(entry.get('description',""))
        detail = getDetail(entry.get("link", ""))
        item["title"] = entry.get("title", "")
        item["link"] = entry.get("link", "")
        item["date"] = published
        item["detail"] = detail
        result.append(item)
    return result
