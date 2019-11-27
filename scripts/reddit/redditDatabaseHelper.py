#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 21:11:20 2019

@author: prathamesh
"""
import mysql.connector
from databaseConnection import database
dbName = "Trenddit"

class redditDataBaseOps:
    def __init__(self, test = False):
        self.test = test
        if(self.test == False):
            self.token = {}
            self.conn = database().getSQLConnection()
    def __del__(self): 
        if(self.conn.is_connected):
            self.conn.close()
    def mysqlConnector(self,databaseName):
        return self.conn
    def addComments(self, commentObject):
        if(self.test == False):
            try:
                conn =self.mysqlConnector(dbName)
                cur = conn.cursor()
                cur.execute("SET NAMES 'utf8mb4';")
                mySql_insert_query = '''INSERT INTO comments (parent_id, name, subreddit_name_prefixed, subreddit_id, total_awards_received, ups, score, author, author_fullname, body, permalink, created_utc, controversiality, offensive_language, hate_speech, speech_type, sentiment)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name = name;'''
       
                recordTuple = tuple(commentObject.values())
                cur.execute(mySql_insert_query, recordTuple)
    #            print(cur._last_executed)
                conn.commit()
                cur.close()
                print("comment: inserted ", commentObject['name']) 
            except mysql.connector.Error as err:
                print("comment: Something went wrong: {}".format(err))
    def addLinks(self, linkObject):
        if(self.test == False):
            mySql_insert_query = """INSERT INTO links VALUES 
                               (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE name = name; """
            recordTuple = tuple(linkObject.values())
            try:
                conn =self.mysqlConnector(dbName)   
                cur = conn.cursor()
                cur.execute("SET NAMES 'utf8mb4';")
                cur.execute(mySql_insert_query, recordTuple)
                conn.commit()
                cur.close()
                print("Links inserted: ", linkObject['name'] ) 
            except mysql.connector.Error as err:
                print("Links: Something went wrong: {}".format(err))
    #        conn.close()