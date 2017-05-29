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
    insert = db.Author.insert_one(
        {
            "Username" : username,
	        "FirstName" : firstname,
	        "LastName" : lastname,
	        "Email" : email,
            "MailingAddress" : address,
            "Affiliation" : affiliation
        }
    )

    query = db.Author.find_one({ "Username" : username})

    if (query is not None):
        print("You have succesfully registered as author: " + username + "!")
    else:
        print("ERROR--We are unable to register an Author with that Username!")

def loginAuthor(db, username):
    print(username)
    authorExists = db.Author.find_one({ "Username" : username })
    if authorExists:
        firstname = authorExists.get(u'FirstName')
        lastname = authorExists.get(u'LastName')
        print("Hello " + firstname + " " + lastname +"!")
        return True
    else:
        print("Sorry, but this username is invalid.  Please try again or register a new Author.")
        return False

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
    print(' ')

    statusRows = ""
    count = 0
    for query in statusQuery:
        status = query.get(u'_id')
        number = query.get(u'count')
        statusRows += str(number) + " " + status + ".\n"
        count += 1
    if (count == 0):
        print("You have no manuscripts!")
    else:
        print(statusRows)


def showAuthorStatusList(db, username):

    statusQuery = db.Manuscript.find({"PrimaryAuthorUsername" : username }, { "_id": 1, "Status": 1, "Title": 1 })

    statusRows = ""
    count = 0
    statusList = list(statusQuery)
    for query in statusList:
        status = query.get(u'Status')
        number = query.get(u'_id')
        title = query.get(u'Title')
        # print(query)
        statusRows += str(number) + "\t\t" + title + " (" + status + ")\n"
        count += 1
    if (count == 0):
        print("You have no manuscripts!")
    else:
        # print("".join(["{:<20}".format(col) for col in cursor.column_names]))
        print("Manuscript\tTitle (status)")
        print("----------------------------------------------------------")
        print(statusRows)


def retractManuscript(db, username, textArray):
    if (len(textArray) == 2):
        man_id = int(textArray[1])
        checkPermission = db.Manuscript.find({"PrimaryAuthorUsername" : username, "_id" : man_id }, { "_id": 1, "PrimaryAuthorUsername": 1})

        if(checkPermission is not None):
            answer = raw_input('Are you sure you want to retract manuscript ' + str(man_id) + '? (yes/no)')

            if (answer == "yes"):
                deleteQuery1 = db.Manuscript.delete_one({ "_id": man_id })
                deleteQuery2 = db.Review.delete_many({ "ManuscriptId": man_id })
                print("Manuscript " + str(man_id) + " removed from system")
        else:
            print("You can only retract Manuscripts that you are the Primary Author of!")
    else:
        print("Please retract a manuscript with the following format: retract <Manuscript ID>")

def submitManuscript(db, username, textArray):

    #find number of editors in the system and get a random editor to assign
    num_editors = db.Editor.find().count()
    all_editors = db.Editor.find()
    rand_editor_num = random.randint(1,num_editors)
    editor_username = ""
    count = 1;
    for query in all_editors:
        if(count == rand_editor_num):
            editor_username = query.get(u'Username')
            break
        count += 1
    print(editor_username)

    #get current date/time
    receivedTime = datetime.now().replace(microsecond=0)

    #get next Id to use
    newest_manuscript = db.Manuscript.find_one({"$query":{},"$orderby":{"_id":-1}})
    highest_id = newest_manuscript.get(u'_id')

    if(len(textArray) == 5):
            insert = db.Manuscript.insert_one(
                {
                    "_id" : highest_id+1,
                    "Title" : textArray[1],
	                "DateReceived" : receivedTime,
                    "Status" : "Submitted",
                    "RICode" : textArray[3],
                    "PrimaryAuthorUsername" : username,
                    "SecondaryAuthors" : None,
                    "EditorUsername" : editor_username,
                    "PagesOccupied" : None,
                    "StartingPage" : None,
                    "Order" : None,
                    "Document" : textArray[4],
                    "JournalIssueYear" : None,
                    "JournalIssuePeriod" : None,
                    "PrimaryAuthorAffiliation" : textArray[2],
                    "DateAcceptReject" : None
                }
            )

            if(insert is not None):
                print("submmited Manuscript " + textArray[1] + " with id = " + str(highest_id+1))

    elif(len(textArray) == 6):
        insert = db.Manuscript.insert_one(
            {
                "_id" : highest_id+1,
                "Title" : textArray[1],
                "DateReceived" : receivedTime,
                "Status" : "Submitted",
                "RICode" : textArray[3],
                "PrimaryAuthorUsername" : username,
                "SecondaryAuthors" : [ textArray[4] ],
                "EditorUsername" : editor_username,
                "PagesOccupied" : None,
                "StartingPage" : None,
                "Order" : None,
                "Document" : textArray[5],
                "JournalIssueYear" : None,
                "JournalIssuePeriod" : None,
                "PrimaryAuthorAffiliation" : textArray[2],
                "DateAcceptReject" : None
            }
        )
        if(insert is not None):
            print("submmited Manuscript " + textArray[1] + " with id = " + str(highest_id+1))


    elif(len(textArray) == 7):
        insert = db.Manuscript.insert_one(
            {
                "_id" : highest_id+1,
                "Title" : textArray[1],
                "DateReceived" : receivedTime,
                "Status" : "Submitted",
                "RICode" : textArray[3],
                "PrimaryAuthorUsername" : username,
                "SecondaryAuthors" : [ textArray[4], textArray[5] ],
                "EditorUsername" : editor_username,
                "PagesOccupied" : None,
                "StartingPage" : None,
                "Order" : None,
                "Document" : textArray[6],
                "JournalIssueYear" : None,
                "JournalIssuePeriod" : None,
                "PrimaryAuthorAffiliation" : textArray[2],
                "DateAcceptReject" : None
            }
        )
        if(insert is not None):
            print("submmited Manuscript " + textArray[1] + " with id = " + str(highest_id+1))

    elif(len(textArray) == 8):
        insert = db.Manuscript.insert_one(
            {
                "_id" : highest_id+1,
                "Title" : textArray[1],
                "DateReceived" : receivedTime,
                "Status" : "Submitted",
                "RICode" : textArray[3],
                "PrimaryAuthorUsername" : username,
                "SecondaryAuthors" : [ textArray[4], textArray[5], textArray[6] ],
                "EditorUsername" : editor_username,
                "PagesOccupied" : None,
                "StartingPage" : None,
                "Order" : None,
                "Document" : textArray[7],
                "JournalIssueYear" : None,
                "JournalIssuePeriod" : None,
                "PrimaryAuthorAffiliation" : textArray[2],
                "DateAcceptReject" : None
            }
        )
        if(insert is not None):
            print("submmited Manuscript " + textArray[1] + " with id = " + str(highest_id+1))
