import requests
import requests.auth
import mysql.connector
from mysql.connector import errorcode
class reddit:
    def __init__(self):
        self.token = {}
        
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
        credentials = self.getCredentials()
        print(credentials)
        tokenDetails = self.getAccessTokenDetails(credentials[0], credentials[1], credentials[2], credentials[3])
        baseURL = "https://oauth.reddit.com"
        headers = {"Authorization": "bearer " + tokenDetails['access_token'] , "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
        response = requests.get(baseURL + api, headers=headers)
        return response.json()
    
        
    def commentObject_t1(self, object_t1):
        if ( object_t1['author'] != "[deleted]" ):
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

            try:
                conn = mysql.connector.connect(host='127.0.0.1', user='root', passwd=None, db='Trenddit', use_unicode=True, charset="utf8", autocommit=True)
                sql = '''SET NAMES 'utf8mb4';INSERT INTO comments (parent_id, name, subreddit_name_prefixed, subreddit_id, total_awards_received, ups, score, author, author_fullname, body, permalink, created_utc, controversiality)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cur = conn.cursor()

                val = tuple(commentObject.values())
                res = cur.execute(sql, val,multi=True)
                res.send(None)
                cur.close()
            except mysql.connector.Error as err:
              if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
              elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
              else:
                print(err)
            else:
              conn.close()
              
            if ( object_t1['replies'] ) : 
                for eachReply in object_t1['replies']['data']['children']:
                    self.getRedditJSONParsed(eachReply)
                                
#    
            
#    CREATE TABLE comments (
#        parent_id varchar(255),
#        name varchar(255) PRIMARY KEY,
#        subreddit_name_prefixed varchar(255),
#        subreddit_id varchar(255),
#        total_awards_received int,
#        ups int,
#        score int,
#        author varchar(255),
#        author_fullname varchar(255),
#        body TEXT,
#        permalink varchar(255),
#        created_utc varchar(255),
#        controversiality int
#    );  
            
#            ALTER TABLE Trenddit.comments MODIFY COLUMN body TEXT
#            CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL;
            
            
                
        return object_t1
    def linkObject_t3(self, object_t3):
        #print("parsing and creating link object")
        return object_t3
    
    def subredditObject_t5(self, object_t5):
        print("parsing and creating Subreddit object")

        return object_t5

    def getRedditJSONParsed(self, redditObject):
        if( redditObject['kind'] == 't1'):
            return self.commentObject_t1(redditObject['data'])
        elif( redditObject['kind'] == 't3'):
            return self.linkObject_t3(redditObject['data'])
        elif( redditObject['kind'] == 't5'):
            return self.subredditObject_t5(redditObject['data'])  
        
    def getRedditData(self, subReddit, outputFileName):
        output = self.getAPIResponse(subReddit)
#       used first elem as it contains comment
        output = output[1]['data']['children']
        for eachChildren in output:
            self.getRedditJSONParsed(eachChildren)
        

reddit().getRedditData('/r/news/comments/ds2smp/abc_news_amy_robach_caught_on_hot_mic_saying/', 'output.json')
