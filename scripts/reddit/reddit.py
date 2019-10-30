import requests
import requests.auth
import json
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
    

    def getRedditData(self, subReddit, outputFileName):
        output = self.getAPIResponse(subReddit)
        databaseName = "Trenddit"
        collectionName = "reddit"
        collection = pythonConnectDB(databaseName, collectionName)
        collection.insert_one(output)
        #with open('data.txt', 'w') as outfile:
            #json.dump(output, outfile, indent=4)


reddit().getRedditData('/r/news/', 'output.json')
