#!/usr/bin/env python

from __future__ import print_function	# print function
from pprint import pprint
from pymongo import MongoClient				# mysql functionality
import sys
import random
import shlex
import time
from datetime import date, datetime, timedelta
from pymongo.collection import ReturnDocument
# {'Username': 'stevencobb', 'FirstName': 'Steven', 'LastName': 'Cobb', 'Email':'neque.Nullam@quis.edu', 'Affiliation': 'Cursus Corp.', 'Retired': false},

def registerAuthor(db, input):
    # fill out all of the information
    if len(input) != 8:
        print("The format for author registration was incorrect.  Please format the query as such:\n register author <username> <fname> <lname> <email> <address> <affiliation>")
        return
    username = input[2]
    fname = input[3]
    lname = input[4]
    email = input[5]
    address = input[6]
    affiliation = input[6]

    # check if the author username is already in the database; if not, create a new author
    usernameExists = db.Author.find_one({"Username": username})
    if usernameExists:
        print("Sorry, but this username has been taken already.  Please try another one.")
        return
    else:
        print("Setting up username")
    result = db.Author.insert_one({"Username": username, "FirstName": fname, "LastName": lname, "Email": email, "MailingAddress": address, "Affiliation": affiliation})
    print(result.inserted_id)
    test = db.Author.find_one({"Username": username})

def loginAuthor(db, username):
    authorExists = db.Author.find_one({"Username": username})
    if authorExists:
        firstname = authorExists.get(u'FirstName')
        lastname = authorExists.get(u'LastName')
        address = authorExists.get(u'MailingAddress')
        print("Hello " + firstname + " " + lastname +"!")
        print("Your current address is: " + address)
        return True
    else:
        print("Sorry, but this username is invalid.  Please try again or register a new author.")
        return False

def showAuthorStatus(db, username):

    results = db.Manuscript.aggregate([
    {"$lookup":
        {"from": "Author", "localField": "PrimaryAuthorUsername", "foreignField": "Username", "as": "author_manuscripts"}
    },
    {"$match":
        {"author_manuscripts.Username": username}
    },
    {"$project":
        {
            "_id": 1,
            "Title": 1,
            "Status": 1,
            "order": {
                "$cond": {
                    "if": { "$eq" : ["$Status", "Received"] }, "then" : 1,
                    "else": {
                        "$cond": {
                            "if": { "$eq" : ["$Status", "Under Review"] }, "then" : 2,
                            "else": {
                                "$cond": {
                                    "if": { "$eq" : ["$Status", "Rejected"] }, "then" : 3,
                                    "else": {
                                        "$cond": {
                                            "if": { "$eq" : ["$Status", "Accepted"] }, "then" : 4,
                                            "else": {
                                                "$cond": {
                                                  "if": { "$eq" : ["$Status", "Typeset"] }, "then" : 5,
                                                  "else": {
                                                      "$cond": {
                                                        "if": { "$eq" : ["$Status", "Scheduled"] }, "then" : 6,
                                                        "else": 7
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    {"$sort":
        {"order": 1},
    },
    {"$group":
        {"_id": "$Status", "count":{"$sum": 1}, "neworder": {"$push": "$order"}},
    },
    {"$sort":
        {"neworder": 1},
    }
    ])

    for doc in results:
        # print(doc)
        status = doc.get(u'_id')
        total = str(doc.get(u'count'))
        print(status + ": " + total)
        # print("_____________________________________")

def showAuthorStatusList(db, username):
    results = db.Manuscript.aggregate([
    {"$lookup":
        {"from": "Author", "localField": "PrimaryAuthorUsername", "foreignField": "Username", "as": "author_manuscripts"}
    },
    {"$match":
        {"author_manuscripts.Username": username}
    },
    {"$project":
        {
            "_id": 1,
            "Title": 1,
            "Status": 1,
            "order": {
                "$cond": {
                    "if": { "$eq" : ["$Status", "Received"] }, "then" : 1,
                    "else": {
                        "$cond": {
                            "if": { "$eq" : ["$Status", "Under Review"] }, "then" : 2,
                            "else": {
                                "$cond": {
                                    "if": { "$eq" : ["$Status", "Rejected"] }, "then" : 3,
                                    "else": {
                                        "$cond": {
                                            "if": { "$eq" : ["$Status", "Accepted"] }, "then" : 4,
                                            "else": {
                                                "$cond": {
                                                  "if": { "$eq" : ["$Status", "Typeset"] }, "then" : 5,
                                                  "else": {
                                                      "$cond": {
                                                        "if": { "$eq" : ["$Status", "Scheduled"] }, "then" : 6,
                                                        "else": 7
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    {"$sort":
        {"order": 1},
    }
    ])

    for doc in results:
        # print(doc)
        status = doc.get(u'Status')
        title = doc.get(u'Title')
        ID = str(doc.get(u'_id'))
        print("Manuscript ID " + ID + ": " + title + " (" + status + ")")

def submitManuscript(db, username, input):
    if len(input) not in [5, 6, 7, 8]:
        print("I'm sorry, but you have put in either too many or too few primary authors.  Please format the query as such:")
        print("submit <title> <Affiliation> <RICode> <author2> <author3> <author4> <filename>")
        return
    title = input[1]
    affiliation = input[2]
    RI = int(input[3])
    document = input[len(input)-1]
    secondaryNumber = len(input) - 5
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # get a random editor
    numEditors = db.Editor.find().count()
    allEditors = db.Editor.find()
    randEditorNum = random.randint(1,numEditors)
    editor = ""
    count = 1;
    for query in allEditors:
        if(count == randEditorNum):
            editor = query.get(u'Username')
            break
        count += 1
    # print(editor)
    # get the next id number
    newestManuscript = db.Manuscript.find_one({"$query":{},"$orderby":{"_id":-1}})
    highestId = newestManuscript.get(u'_id')
    ID = highestId + 1
    # create manuscript to insert
    secondaryAuthors = []
    manuscriptObject = {"_id": ID, "Title": title,"DateReceived": timestamp,"Status": "Received","RICode": RI,"PrimaryAuthorUsername": username, "EditorUsername": editor,"PagesOccupied": None,"StartingPage": None,"Order": None,"Document": document,"JournalIssueYear": None,"JournalIssuePeriod": None, "PrimaryAuthorAffiliation": affiliation, "DateAcceptReject": None}
    # print(manuscriptObject)
    if secondaryNumber != 0:
        print("there is 1 primary author at least!")
        for x in range(secondaryNumber):
            secondaryAuthors.append(input[4+x])
        manuscriptObject = {"_id": ID, "Title": title,"DateReceived": timestamp,"Status": "Received","RICode": RI,"PrimaryAuthorUsername": username, "SecondaryAuthors": secondaryAuthors, "EditorUsername": editor,"PagesOccupied": None,"StartingPage": None,"Order": None,"Document": document,"JournalIssueYear": None,"JournalIssuePeriod": None, "PrimaryAuthorAffiliation": affiliation, "DateAcceptReject": None}
    # print(manuscriptObject)
    # check if manuscript is already there
    manuscriptExists = db.Manuscript.find_one({"PrimaryAuthorUsername": username, "Title": title})
    if manuscriptExists:
        print("You have already submitted a manuscript with this same title.  Please submit a manuscript with a different title.")
        return
    # check if there are enough reviewers
    reviewerCount = db.ReviewerInterests.find({"RICode": RI}).count()
    if reviewerCount < 3:
        print("There must be more than three reviewers with an interest in this field for this manuscript to be submitted.")
        return
    submitManuscript = db.Manuscript.insert_one(manuscriptObject)
    if submitManuscript:
        print("You just submitted Manuscript " + str(submitManuscript.inserted_id))
    else:
        print("Something occurred during insertion and we were unable to submit the manuscript.  Please try again.")
        return
    # update author affiliation
    affiliationUpdate = db.Author.find_one_and_update({"Username": username}, {"$set": {"Affiliation": affiliation}}, return_document=ReturnDocument.AFTER)
    if not affiliationUpdate:
        print("Unable to update author affiliation")
        return

def retractManuscript(db, username, input):
    if len(input) != 2:
        print("Please format the query correctly:\n retract <manuscriptId>")
        return
    manuscript = int(input[1])
    isAssigned = db.Manuscript.find_one({"_id": manuscript, "PrimaryAuthorUsername": username, "Status": {"$nin": ["Published"]}})
    if not isAssigned:
        print("You are either not associated with this manuscript, or it has already been published")
        return
    verification = raw_input("Are you sure you want to retract manuscript " + str(manuscript) + "? (yes/no)\n")
    if verification == "no":
        print("Ok. Manuscript will not be retracted.")
        return
    elif verification != "yes":
        print("The answer must be either yes or no.  Please try retracting the manuscript again.")
        return
    if verification == "yes":
        deleteManuscript = db.Manuscript.delete_one({ "_id": manuscript })
        deleteReviews = db.Review.delete_many({ "ManuscriptId": manuscript })
        test = db.Review.find({ "ManuscriptId": manuscript }).count()
        if test > 0:
            print("Note: not all reviews deleted for manuscript")
        print("Retracted manuscript " + str(manuscript))
