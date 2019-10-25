import urllib.request as url

gUrl = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen"
baseGUrl = "https://news.google.com/"; 


# user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'

# # header variable
# headers = { 'User-Agent' : user_agent }

# # creating request
# req = url.Request(gUrl, None, headers)

# page = url.urlopen(req).read().decode('utf-8')

# # body = re.findall(r'/<body[^>]*>(.*?)<\/body>/is', html)

# # print(body[0:1000])

#
#class RelatedArticleClass:
#    def __init__(self, url, time, source, text):
#       self.url = url
#       self.time = time
#       self.source = source
#       self.text = text
#
#class NewsArticleClass:
#    def __init__(self, text, relatedArticles):
#       self.text = text
#       self.relatedArticles = relatedArticles



# for parsing string to date format
def convertDateToJson( date ):
    from dateutil import parser as dateParser
    import datetime
    if isinstance( date, str):
        date = dateParser.parse(date)
    if isinstance(date, datetime.datetime):
        return date.__str__()

# string utils
def removeMinWordsFromListOfString( listSring , noOfWords = 1):
    return  ' '.join([ eachLine for eachLine in listSring if len(str(eachLine).split()) > noOfWords])

# Mongo db utils
# python -> mongo connect
def pythonConnectDB( databaseName, collectionName):
    import pymongo
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[databaseName]
    dblist = myclient.list_database_names()
    if databaseName in dblist:
        print(databaseName + " database exists.")
    else:
        raise ValueError(databaseName + " database does not exist")
    return mydb[collectionName]


def gnewsCrawl(gNewsUrl):
    from lxml import html
    import requests
    import datetime

#    session = requests.Session()  # so connections are recycled

    page = requests.get(gNewsUrl).content
    tree = html.fromstring(page)

    outputNewsArr = []
    news = tree.xpath('.//*[@class="xrnccd"]')
    relatedNewsHtml =  tree.xpath('.//*[@class="SbNwzf"]')

    for index, relatedNews in enumerate(relatedNewsHtml):
        articles = relatedNews.xpath('.//article')
        firstNews = relatedNews.xpath('./parent::*/article')[0]
        articles.append(firstNews)
        relatedArticles = []
        for eachArticleIndex, eachArticle  in enumerate(articles):
            href = eachArticle.xpath('./*[@class="VDXfz"][1]/@href')[0]
    #        resp = session.head(baseGUrl +href[2:], allow_redirects=True)
    #        print(resp.url)
            time = convertDateToJson(eachArticle.xpath('.//time[1]/@datetime')[0])
            source = eachArticle.xpath('.//*[@class="SVJrMe"][1]/a[1]')[0].text_content()
            text  = eachArticle.xpath('.//text()')
            text = removeMinWordsFromListOfString(text)
            relatedArticles.append({
			"index": eachArticleIndex,
                        "href": href,
                        "time": time,
                        "source": source,
                        "text:": text,
                    })
        txt = firstNews.xpath('.//text()')
        outputNewsArr.append({
                "text": removeMinWordsFromListOfString(txt), 
                "relatedArticles": relatedArticles})

    json_data ={
            "news": outputNewsArr,
            "scriptTime": convertDateToJson(datetime.datetime.now())
            }

    print("Done")

    for i in outputNewsArr[0:1]:
        print("text : " + str(i['text']))
    return json_data



def scheduleJob():
    from apscheduler.schedulers.blocking import BlockingScheduler
    
    databaseName = "Trenddit"
    collectionName = "gnews"
    collection = pythonConnectDB(databaseName, collectionName)

    def saveGnewsData():
        print ("job Started")
        json_data = gnewsCrawl("https://news.google.com/?hl=en-US&gl=US&ceid=US:en")
        collection.insert_one(json_data)
        print ("job Ended")

    scheduler = BlockingScheduler()
    scheduler.add_job(saveGnewsData, 'interval',  minutes=1)
    scheduler.start()

scheduleJob()
