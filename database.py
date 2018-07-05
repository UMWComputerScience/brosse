#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 13:50:34 2018

@author: bryceanderson
"""
"""
To-Do:
    - add some sort of tracking progress system
    - set up skeleton code for database
    """
import psycopg2

conn = psycopg2.connect(host="", database="tweets", user="postgres") #Need database name and rest or params



def get_Tweets():
    cur = conn.cursor()
    cur.execute("Select UserID from Users")
    userID = cur.fetchone()
    """Loop through Users table collecting the User ID"""
    while userID is not None:
        """Look at Index table and pull tweets rows for userID"""
        cur.execute("Select Row from Index")
        rows = cur.fetchall()
        text = ""
        for row in rows:
            cur.execute("Select Text from Tweets where userID=UserID limit 1 offset row-1")
            text += cur.fetchone()
        