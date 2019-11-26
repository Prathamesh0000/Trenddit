#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:05:30 2019

@author: prathamesh
"""
dbName = "Trenddit"
import mysql.connector
class database:
    def __init__(self):
        print("database class init")
        self.mySQLConn = None
        self.mongoclient = None
    def __del__(self):
        if(self.mySQLConn) :
#            self.mySQLConn.close()
            print("connection closed with sql")
        
    def getSQLConnection(self):
        if(self.mySQLConn) :
            return self.mySQLConn
        else:
            self.mySQLConn = mysql.connector.connect(host='127.0.0.1', user='admin', passwd='password', db=dbName, use_unicode=True, charset="utf8", autocommit=True)
            if self.mySQLConn.is_connected():
                print("connection extablished with sql")
            return self.mySQLConn
    
    def getMongoConnection(self, databaseName, collectionName):
        import pymongo
        if(self.mongoclient) :
            self.mongoclient;
        else:
            self.mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")

        mydb = self.mongoclient[databaseName]
        dblist = self.mongoclient.list_database_names()
        if databaseName in dblist:
            print(databaseName + " database exists.")
        else:
            raise ValueError(databaseName + " database does not exist")
        return mydb[collectionName]