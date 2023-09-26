import json
import requests
import datetime
from xmlparser import removeHTMLTags


class NaverAPIAuth:
    clientId = ""
    clientSecret = ""

    def __init__(self):
        success = self.getAuth()

        if not success:
            raise Exception("Failed to get Auth")

    def checkNaverAPIAuth(self, clientId, clientSecret):
        if clientId == "":
            return 1
        if clientSecret == "":
            return 1
        return 0

    def extractAuth(self, fileSystem, content):
        errorCode = fileSystem(content)
        return errorCode

    def extractAuthFromJsonFormat(self, content):
        result = json.loads(content)
        return result["clientId"], result["clientSecret"]

    def extractAuthFromGitlabCDVar(self, content):
        result = content.split(".")
        return result[0].strip(), result[1].strip()

    def getAuthFromFile(self, filePath):
        try:
            with open(filePath, "r") as f:
                clientId, clientSecret = self.extractAuth(self.extractAuthFromGitlabCDVar, f.read())
                if self.checkNaverAPIAuth(clientId, clientSecret):  # error occur is 1
                    return False
                self.clientId = clientId
                self.clientSecret = clientSecret
        except Exception as e:
            print("[ERROR] {}".format(e))

        return True

    def getAuth(self):
        return self.getAuthFromFile("naverapi.key")

    def getClientId(self):
        return self.clientId

    def getClientSecret(self):
        return self.clientSecret


def requestNaverAPI(keyword):
    requestURL = "https://openapi.naver.com/v1/search/news.json"
    requestParams = {"query": keyword, "display": 30, "sort": "date"}
    auth = NaverAPIAuth()
    authHeaders = {"X-Naver-Client-Id": auth.getClientId(), "X-Naver-Client-Secret": auth.getClientSecret()}
    try:
        resp = requests.get(requestURL, params=requestParams, headers=authHeaders)
        result = resp.text
    except Exception as e:
        print("requests error!", e)
        result = ""

    return result  # respose Json Result


def parseNaverAPIResultFromJson(jsonData):
    result = []
    # print(jsonData)
    items = jsonData["items"] if "items" in jsonData.keys() else []

    for item in items:
        entry = {"title": "", "date": "", "link": "", "detail": None}
        entry["title"] = "[네이버 뉴스] " + removeHTMLTags(item["title"])
        entry["link"] = item["link"]
        entry["detail"] = {"description": removeHTMLTags(item["description"])}
        # date 가공
        entry["date"] = datetime.datetime.strptime(item["pubDate"], "%a, %d %b %Y %H:%M:%S %z")
        print("title: ", entry["title"])
        print("date: ", entry["date"])
        result.append(entry)

    return result


def parseNaverAPIResult(raw, parseType="json"):
    result = []
    if parseType == "json":
        jsonData = json.loads(raw)
        result = parseNaverAPIResultFromJson(jsonData)
    return result


def getContentFromNaver(keyword):
    raw = requestNaverAPI(keyword)
    result = parseNaverAPIResult(raw, "json")
    return result
