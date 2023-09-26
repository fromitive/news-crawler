import requests
import xml.etree.ElementTree as ET
import urllib.parse
from getDetail import getDetail
from bs4 import BeautifulSoup
from datetime import datetime


# XML parser
def requestXML(url):
    req = requests.get(url, timeout=5)
    root = ET.fromstring(req.text)
    return root


def getEntityGoogle(xmlRoot):
    children = list(xmlRoot)
    Entity = children[4:]
    return Entity


# example


def removeHTMLTags(text):
    result = text
    removeElements = ["<b>", "</b>", "&quot;", "&amp;", "&#39;"]
    for removeElement in removeElements:
        result = result.replace(removeElement, "")

    return result


def getTitleAndLinkGoogle(xmlRoot):
    children = getEntityGoogle(xmlRoot)
    result = []
    for child in children:
        entry = {"title": "", "date": "", "link": "", "detail": None}
        # title
        title = child[1].text
        title = removeHTMLTags(title)
        print("title:\t", title)

        # date
        strpublished = child[3].text
        published = datetime.strptime(strpublished, "%Y-%m-%dT%H:%M:%SZ")
        print("date:\t", published)

        # link
        url = child[2].attrib["href"]
        encodedURL = url[url.find("url=") + 4 : url.find("&ct=ga")]
        originurl = urllib.parse.unquote(encodedURL)
        print("link:\t", originurl)
        # print("detail: ")
        # detail
        content = getDetail(originurl)
        # print(content)

        entry["title"] = title
        entry["date"] = published
        entry["link"] = originurl
        entry["detail"] = content
        result.append(entry)
    return result


def getContent(url):
    root = requestXML(url)
    result = getTitleAndLinkGoogle(root)
    return result
