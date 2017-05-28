#!/usr/bin/env python

from __future__ import print_function	# print function
from pprint import pprint
from pymongo import MongoClient				# mysql functionality
import sys
import random
import shlex
import time
from datetime import date, datetime, timedelta

def registerAuthor(db, username, firstname, lastname, address, email, affiliation):
    # insert = db.Author.insert_one(
    #     {
    #         "Username" : username,
	#         "FirstName" : firstname,
	#         "LastName" : lastname,
	#         "Email" : email,
    #         "MailingAddress" : address,
    #         "Affiliation" : affiliation
    #     }
    # )

    query = db.Author.find_one({ "Username" : username})

    if (query is not None):
        print("You have succesfully registered as author: " + username + "!")
    else:
        print("ERROR--We are unable to register an Author with that Username!")

def showAuthorStatus(db, username):
    # statusQuery = db.Manuscript.find({"PrimaryAuthorUsername" : "whileminasavage"}, { "_id": 1, "Status": 1 })
    statusQuery  = db.Manuscript.aggregate([
        { "$match" :
            { "PrimaryAuthorUsername" : username } },
        { "$group" : {
            "_id":"$Status", "count":{ "$sum": 1}
            }
        }
    ])
    print("Below, you will find the number of manuscripts in each phase \nof review (i.e status) that are under your guidance:")

    statusRows = ""
    count = 0
    for query in statusQuery:
        print(query)
        status = query.get(u'_id')
        number = query.get(u'count')
        statusRows += str(number) + " " + status + ". "
        count += 1
    if (count == 0):
        print("You have no manuscripts!")
    else:
        print(statusRows)
