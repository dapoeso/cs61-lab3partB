# Author.py
# Author driver for when an author logs in to the system.

from __future__ import print_function	# print function
from pprint import pprint
from pymongo import MongoClient				# mysql functionality
import sys
import random
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
        print("ERROR--We are unable to register and Author with that Username!")

def showStatus(db, username):
    # statusQuery = db.Manuscript.find({"PrimaryAuthorUsername" : "whileminasavage"}, { "_id": 1, "Status": 1 })
    statusQuery  = db.Manuscript.aggregate([
        { "$match" :
            { "PrimaryAuthorUsername" : "whileminasavage" } },
        { "$group" : {
            "_id":"$Status", "count":{ "$sum": 1}
            }
        }
    ])
    print("Below, you will find the number of manuscripts in each phase \nof review (i.e status) that are under your guidance:")
    print(' ')

    statusRows = ""
    count = 0
    for query in statusQuery:
        status = query.get(u'_id')
        number = query.get(u'count')
        statusRows += str(number) + " " + status + ". "
        count += 1
    if (count == 0):
        print("You have no manuscripts!")
    else:
        print(statusRows)

    print(' ')
    print("Below, you will also find a table showing the manuscript \nnumber corresponding to the status that manuscript is in:")
    print(' ')

    statusQuery = db.Manuscript.find({"PrimaryAuthorUsername" : "whileminasavage"}, { "_id": 1, "Status": 1 })

    statusRows = ""
    count = 0
    statusList = list(statusQuery)
    for query in statusList:
        status = query.get(u'Status')
        number = query.get(u'_id')
        # print(query)
        statusRows += "Manuscript Number: " + str(number) + "\t" + "Status: " + status + "\n"
        count += 1
    if (count == 0):
        print("You have no manuscripts!")
    else:
        # print("".join(["{:<20}".format(col) for col in cursor.column_names]))
        print("----------------------------")
        print(statusRows)
