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
    statusQuery = db.Manuscript.find({"PrimaryAuthorUsername" : "whileminasavage"})

    print("Below, you will find the number of manuscripts in each phase \nof review (i.e status) that are under your guidance:")

    statusRows = ""
    count = 0
    for row in statusQuery:
        array = ["{}".format(col) for col in row]
        print("===========================")
        print(array)
        print("===========================")
        statusRows += array[12] + " " + array [0] + ". "
        # pprint(row)
        count += 1
    if (count == 0):
        print("You have no manuscripts!")
    else:
        print(statusRows)
