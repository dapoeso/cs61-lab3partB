#!/usr/bin/env python

from __future__ import print_function	# print function
from pprint import pprint
from pymongo import MongoClient				# mysql functionality
import sys
import random
import shlex
import time
from datetime import date, datetime, timedelta
# {'Username': 'stevencobb', 'FirstName': 'Steven', 'LastName': 'Cobb', 'Email':'neque.Nullam@quis.edu', 'Affiliation': 'Cursus Corp.', 'Retired': false},

def registerReviewer(db, input):
    # fill out all of the information
    username = None
    fname = None
    lname = None
    email = None
    affiliation = None
    retired = 0
    riCodes = len(input) - 7
    if len(input) >= 8 and len(input) <= 10:
        username = input[2]
        fname = input[3]
        lname = input[4]
        email = input[5]
        affiliation = input[6]
        retired = 0
    else:
        print("Please format your query correctly.")
        return
    # print(input)
    print(fname, lname)

    # check if the reviewer username is already in the database; if not, create a new reviewer
    usernameExists = db.Reviewer.find_one({"Username": username})
    if usernameExists:
        print("Sorry, but this username has been taken already.  Please try another one.")
        return
    else:
        print("Yay!")
    result = db.Reviewer.insert_one({"Username": username, "FirstName": fname, "LastName": lname, "Email": email, "Affiliation": affiliation, "Retired": retired})
    print(result.inserted_id)
    test = db.Reviewer.find_one({"Username": username})
    print(test)
    # add all of the RI codes that correspond to the reviewer
    for x in range(0, riCodes):
        insertRI(db, username, int(input[7+x]))

def insertRI(db, username, RI):
    # check if the RI code is valid
    RIExists = db.RICodes.find_one({"code": RI})
    if not RIExists:
        print("Sorry, but this RI Code is invalid")
    #check if RI already exists for that reviewer; if not, insert it
    interestExists = db.ReviewerInterests.find_one({"ReviewerUsername": username, "RICode": RI})
    if interestExists:
        print("Sorry, but this reviewer already has this RI Code.")
        return
    result = db.ReviewerInterests.insert_one({"ReviewerUsername": username, "RICode": RI})
    print(result.inserted_id)

def showReviewerStatus(db, username):

    results = db.Manuscript.aggregate([
    {"$lookup":
        {"from": "Review", "localField": "_id", "foreignField": "ManuscriptId", "as": "reviewer_reviews"}
    },
    {"$match":
        {"reviewer_reviews.ReviewerUsername": username}
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
        {"_id": "$Status", "count":{"$sum": 1}},
    }
    ])

    for doc in results:
        status = doc.get(u'_id')
        total = str(doc.get(u'count'))
        print(status + ": " + total)
        # print("_____________________________________")

def showReviewerStatusList(db, username):

    results = db.Manuscript.aggregate([
    {"$lookup":
        {"from": "Review", "localField": "_id", "foreignField": "ManuscriptId", "as": "reviewer_reviews"}
    },
    {"$match":
        {"reviewer_reviews.ReviewerUsername": username}
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
        status = doc.get(u'Status')
        title = doc.get(u'Title')
        ID = str(doc.get(u'_id'))
        print("Manuscript ID " + ID + ": " + title + " (" + status + ")")
        # print("_____________________________________")
# def showAuthorStatus(db, username):
#     # statusQuery = db.Manuscript.find({"PrimaryAuthorUsername" : "whileminasavage"}, { "_id": 1, "Status": 1 })
#     statusQuery  = db.Manuscript.aggregate([
#         { "$match" :
#             { "PrimaryAuthorUsername" : username } },
#         { "$group" : {
#             "_id":"$Status", "count":{ "$sum": 1}
#             }
#         }
#     ])
#     print("Below, you will find the number of manuscripts in each phase \nof review (i.e status) that are under your guidance:")
#
#     statusRows = ""
#     count = 0
#     for query in statusQuery:
#         print(query)
#         status = query.get(u'_id')
#         number = query.get(u'count')
#         statusRows += str(number) + " " + status + ". "
#         count += 1
#     if (count == 0):
#         print("You have no manuscripts!")
#     else:
#         print(statusRows)
