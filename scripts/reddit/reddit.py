import requests
import requests.auth
import json
import mysql.connector
test = False
class reddit:
    def __init__(self):
        self.token = {}
        self.conn = mysql.connector.connect(host='127.0.0.1', user='root', passwd=None, db='Trenddit', use_unicode=True, charset="utf8")
        
    def mysqlConnector(self,databaseName):
        
        cnx = mysql.connector.connect(user='root', password='D@hanu2009',
                              host='localhost',
                              database=databaseName,autocommit=True)
        return cnx
    
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
        
    
        
    def commentObject_t1(self, object_t1):

        print("t1:parsing and creating Comment object")
        
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
            
            
            try:
                sql = '''show warnings;SET NAMES utf8mb4;INSERT INTO comments (parent_id, name, subreddit_name_prefixed, subreddit_id, total_awards_received, ups, score, author, author_fullname, body, permalink, created_utc, controversiality)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                self.cur = self.conn.cursor()

                val = tuple(commentObject.values())
                self.cur.execute(sql, val, multi=True)
                self.conn.commit()
                self.cur.close()
            except mysql.connector.Error as error:    
                print("Failed to insert into MySQL table {}".format(error))
            
            
            if ( object_t1['replies'] ) : 
                for eachReply in object_t1['replies']['data']['children']:
                    self.getRedditJSONParsed(eachReply)
                
        return object_t1
    
    def linkObject_t3(self, object_t3):
        print("t3:parsing and creating link object")
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
        mySql_insert_query = """INSERT INTO links VALUES 
                           (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        recordTuple = tuple(final.values())
        conn =self.mysqlConnector("trenddit")
        cur = conn.cursor()
        cur.execute(mySql_insert_query, recordTuple)
        conn.commit()
        cur.close()
        conn.close()
        
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
        
        for eachElem in output['data']['children']:
            self.getRedditJSONParsed(eachElem)

reddit().getRedditData('/r/news/')