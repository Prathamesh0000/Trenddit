import requests
import requests.auth
import json
#import mysql.connector
from mysql.connector import errorcode
test = False


# influencers (+/-)
# Attackers
# neutral
    
#CDF

# /Donald 
# /debateCommunism
#Two sample ks test
comment_score_array = []

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

def textClassification(text):
    sentiment_analyzer_scores(text)



def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
#    print(str(score))
    return score

def plotForData(data):
    import numpy as np
    import matplotlib.pyplot as plt
    num_bins = 50
    counts, bin_edges = np.histogram (data, bins=num_bins, normed=True)
    
    # Now find the cdf
    cdf = np.cumsum(counts)
    
    # And finally plot the cdf
    plt.plot(bin_edges[1:], cdf)
    
    plt.show()
#import mysql.connector
#class database:
#    def __init__(self):
#        print("database class init")
#        self.mySQLConn = None
#        self.mongoclient = None
#    def __del__(self):
#        if(self.mySQLConn) :
##            self.mySQLConn.close()
#            print("connection closed with sql")
#        
#    def getSQLConnection(self):
#        if(self.mySQLConn) :
#            return self.mySQLConn
#        else:
#            self.mySQLConn = mysql.connector.connect(host='127.0.0.1', user='admin', passwd='password', db=dbName, use_unicode=True, charset="utf8", autocommit=True)
#            if self.mySQLConn.is_connected():
#                print("connection extablished with sql")
#            return self.mySQLConn
#    
#    def getMongoConnection(self, databaseName, collectionName):
#        import pymongo
#        if(self.mongoclient) :
#            self.mongoclient;
#        else:
#            self.mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
#
#        mydb = self.mongoclient[databaseName]
#        dblist = self.mongoclient.list_database_names()
#        if databaseName in dblist:
#            print(databaseName + " database exists.")
#        else:
#            raise ValueError(databaseName + " database does not exist")
#        return mydb[collectionName]
#from databaseConnection import database
 
#class redditDataBaseOps:
#    def __init__(self):
#        self.token = {}
#        self.conn = database().getSQLConnection()
#    def __del__(self): 
#        self.conn.close()
#    def mysqlConnector(self,databaseName):
#        return self.conn
#    def addComments(self, commentObject):
#        try:
#            conn =self.mysqlConnector(dbName)
#            cur = conn.cursor()
#            cur.execute("SET NAMES 'utf8mb4';")
#            mySql_insert_query = '''INSERT INTO comments (parent_id, name, subreddit_name_prefixed, subreddit_id, total_awards_received, ups, score, author, author_fullname, body, permalink, created_utc, controversiality)
#            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = name;'''
#   
#            recordTuple = tuple(commentObject.values())
#            cur.execute(mySql_insert_query, recordTuple)
##            print(cur._last_executed)
#            conn.commit()
#            cur.close()
#            print("comment: inserted ", commentObject['name']) 
#        except mysql.connector.Error as err:
#            print("comment: Something went wrong: {}".format(err))
#    def addLinks(self, linkObject):
#        mySql_insert_query = """INSERT INTO links VALUES 
#                           (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name = name; """
#        recordTuple = tuple(linkObject.values())
#        try:
#            conn =self.mysqlConnector(dbName)   
#            cur = conn.cursor()
#            cur.execute("SET NAMES 'utf8mb4';")
#            cur.execute(mySql_insert_query, recordTuple)
#            conn.commit()
#            cur.close()
#            print("Links inserted: ", linkObject['name'] ) 
#        except mysql.connector.Error as err:
#            print("Links: Something went wrong: {}".format(err))
##        conn.close()
    
    
class reddit:
    def __init__(self, redditConn):
        self.token = {}
#        self.conn = database().getSQLConnection()
        self.redditDatabase = redditConn
    def __del__(self): 
#        self.conn.close()
        print("Destructor called") 
    def mysqlConnector(self,databaseName):
        return self.conn

    def getAccessTokenDetails(self, appId, secretKey, username, password):
        client_auth = requests.auth.HTTPBasicAuth(appId , secretKey)
        post_data = {"grant_type": "password", "username": username, "password": password}
        headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        self.token = response.json()
        return self.token
    def getCredentials(self):
        filepath = 'reddit-auth.txt'
        credentials = []
        with open(filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                credentials.append(line.strip())
                line = fp.readline()
                cnt += 1
        return credentials
    def getAPIResponse(self, api):
        if(test):
            with open("reddit_test.json", 'r') as f:
                #response = json.load(f)
                response = f.read()
                #use this only when reading from json file otherwise don't use below statement
                response = json.loads(response)
                return response
        else:
            credentials = self.getCredentials()
            print(credentials)
            tokenDetails = self.getAccessTokenDetails(credentials[0], credentials[1], credentials[2], credentials[3])
            baseURL = "https://oauth.reddit.com"
            headers = {"Authorization": "bearer " + tokenDetails['access_token'] , "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
            response = requests.get(baseURL + api, headers=headers)
            return response.json()
        
    
        
    def commentObject_t1(self, object_t1, linkObj):
        if 'author' in object_t1:
            if ( object_t1['author'] != "[deleted]" ):
#                print("t1:parsing and creating Comment object")
                print( object_t1['parent_id'] + "->" + object_t1['name'])
                commentObject = {}
                
                commentObject['parent_id'] = object_t1['parent_id']          # parent Id : Foreign key[comments]
                commentObject['name'] =  object_t1['name']                   # name Id   : Primary key[comments]
                
                commentObject['subreddit_name_prefixed'] = object_t1['subreddit_name_prefixed'] 
                commentObject['subreddit_id'] =  object_t1['subreddit_id']   # subreddit Id: Foreign key[subreddit]
        
        
                commentObject['total_awards_received'] =  object_t1['total_awards_received']
                commentObject['ups'] =  object_t1['ups']
        
                commentObject['score'] =  object_t1['score']
        
                commentObject['author'] =  object_t1['author']
                commentObject['author_fullname'] =  object_t1['author_fullname'] if 'author_fullname' in object_t1 else ""
        
                commentObject['body'] =  object_t1['body']
        
                commentObject['permalink'] =  object_t1['permalink']
                commentObject['created_utc'] = object_t1['created_utc']
                commentObject['controversiality'] =  object_t1['controversiality'] if 'controversiality' in object_t1 else -1
                
                text_score = sentiment_analyzer_scores(commentObject['body'])
                score = {
                    'obj': commentObject,
                }
                
                
                for i in text_score:
                    score[i] = text_score[i]
                comment_score_array.append(score)
                self.redditDatabase.addComments(commentObject)
                if ( object_t1['replies'] ) : 
                    for eachReply in object_t1['replies']['data']['children']:
                        self.commentObject_t1(eachReply['data'], linkObj)
                
                
    def linkObject_t3(self, object_t3, linkObj):
#        print("t3:parsing and creating link object")
        final = {}
        final['id'] = object_t3['id']
        final['subreddit_id'] = object_t3['subreddit_id'] #primary key [links]
        final['name'] = object_t3['name'] #primary key [links]
        final['subreddit_name_prefixed'] = object_t3['subreddit_name_prefixed']
        final['url'] = object_t3['url']
        final['domain'] = object_t3['domain']
        final['total_awards_received'] = object_t3['total_awards_received']
        final['ups'] = object_t3['ups']
        final['score'] = object_t3['score']
        final['pinned'] =  object_t3['pinned']
        final['author'] = object_t3['author']
        final['author_fullname'] = object_t3['author_fullname']
        final['title'] = object_t3['title']
        final['permalink'] = object_t3['permalink']
        final['created_utc'] = object_t3['created_utc']
        final['num_comments'] = object_t3['num_comments']
        final['num_crossposts'] = object_t3['num_crossposts']
        #final['downs'] = object_t3['downs']
        #final['is_video'] = object_t3['is_video']
        #final['view_count'] = object_t3['view_count']
        self.redditDatabase.addLinks(final)

        reddit(self.redditDatabase).getRedditData(final['permalink'], object_t3)
        
        
    def subredditObject_t5(self, object_t5, object_t3):
        print("parsing and creating Subreddit object")
        return object_t5
    def subredditObject_More(self, object_More, linkObj):
        print("-----------------------more")
        moreChildrenAPIEndPoint = "/api/morechildren"
        children = object_More['children']
        moreChildId = object_More['id']
        link_id = linkObj['id']
        
        print(self.getAPIResponse( moreChildrenAPIEndPoint + '?children=' + ','.join(children)+ "&link_id=" + link_id+ "&id=" +  moreChildId))
        
    def getRedditJSONParsed(self, redditObject, linkObj):
        if( redditObject['kind'] == 't1'):
            return self.commentObject_t1(redditObject['data'], linkObj)
        elif( redditObject['kind'] == 't3'):
            return self.linkObject_t3(redditObject['data'], linkObj)
        elif( redditObject['kind'] == 't5'):
            return self.subredditObject_t5(redditObject['data'], linkObj)  
        elif( redditObject['kind'] == 'more'):
            return self.subredditObject_More(redditObject['data'], linkObj)
        
    def getRedditData(self, subReddit, linkObj):
        output = self.getAPIResponse(subReddit)
        if isinstance(output, list):
            #used first elem as it contains comment
            output = output[1]
#        elif 'data' in output:
        for eachElem in output['data']['children']:
            self.getRedditJSONParsed(eachElem, linkObj)
#        else:
#            print(output)
#        print(output)

from redditDatabaseHelper import redditDataBaseOps
sub = "/r/The_Donald/"
print(sub)  
reddit(redditDataBaseOps()).getRedditData(sub, None)




# Analyisi

#comment_score_array.sort(key=lambda x: x['score']['compound'], reverse=True)

comment_compound = sorted(comment_score_array, key=lambda x: x['compound'], reverse=True)

comment_compound_positive = []
comment_compound_negative = []
comment_compound_neutral = []


for i in range(len(comment_compound)):
  if comment_compound[i]['compound'] > 0:
    comment_compound_positive.append(comment_compound[i])
  if comment_compound[i]['compound'] < 0:
    comment_compound_negative.append(comment_compound[i])
  if comment_compound[i]['compound'] == 0:
    comment_compound_neutral.append(comment_compound[i])

comment_compound_positive_score_avg = sum([ i['obj']['score'] for i in comment_compound_positive ]) / len(comment_compound_positive)
comment_compound_negative_score_avg = sum([ i['obj']['score'] for i in comment_compound_negative ]) / len(comment_compound_negative)
comment_compound_neutral_score_avg = sum([ i['obj']['score'] for i in comment_compound_neutral ]) / len(comment_compound_neutral)

tot = [ i['compound'] for i in comment_compound ]   
tot_avg = sum(tot)/len(tot)


pos = [ i['compound'] for i in comment_compound_positive ]   
pos_avg = sum(pos)/len(pos)
      
neg = [ i['compound'] for i in comment_compound_negative ]   
neg_avg = sum(neg)/len(neg)

      
neu = [ i['compound'] for i in comment_compound_neutral ]   
neu_avg = sum(neu)/len(neu)


# not usefull

plotForData(tot)
print("total senti cdf plot ^")


plotForData(neg)
print("negative senti cdf plot ^")


plotForData(pos)
print("positive senti cdf plot ^")


plotForData(neu)
print("neu senti cdf plot ^")


# not usefull

plotForData([ i['obj']['score'] for i in comment_compound ])
print("total reddit score senti cdf plot ^")


comment_compound_negative_reddit_score = [ i['obj']['score']  for i in comment_compound if i['compound'] < 0]
plotForData(comment_compound_negative_reddit_score)
print("negative reddit score senti cdf plot ^")


comment_compound_positive_reddit_score = [ i['obj']['score']  for i in comment_compound if i['compound'] > 0]
plotForData(comment_compound_positive_reddit_score)
print("positive reddit score senti cdf plot ^")


comment_compound_neutral_reddit_score = [ i['obj']['score']  for i in comment_compound if i['compound'] == 0]
plotForData(comment_compound_neutral_reddit_score)
print("neutral reddit score senti cdf plot ^")


import powerlaw
 
results = powerlaw.Fit(tot)
print(results.power_law.alpha)
print(results.power_law.xmin)
R, p = results.distribution_compare('power_law', 'lognormal')



# importing the required module 
import matplotlib.pyplot as plt  
  
# plotting the points  
plt.plot([ i['compound'] for i in comment_compound ]  , [ i['obj']['score'] for i in comment_compound ]  ) 
  
# naming the x axis 
plt.xlabel('compound score senti') 
# naming the y axis 
plt.ylabel('upvotes') 
  
# giving a title to my graph 
plt.title(' senti/ upvotes') 
  
# function to show the plot 
plt.show() 
