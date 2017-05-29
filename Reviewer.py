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
        print("Please format your query correctly. You may have included too many or too few RI codes (1 minimum, 3 maximum).")
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

def loginReviewer(db, username):
    reviewerExists = db.Reviewer.find_one({"Username": username})
    if reviewerExists:
        retired = reviewerExists.get(u'Retired')
        if retired:
            print("Sorry, but this reviewer has retired.")
            return False
        else:
            firstname = reviewerExists.get(u'FirstName')
            lastname = reviewerExists.get(u'LastName')
            print("Hello " + firstname + " " + lastname +"!")
            return True
    else:
        print("Sorry, but this username is invalid.  Please try again or register a new reviewer.")
        return False

def retireReviewer(db, username):
    newReview = db.Reviewer.find_one_and_update({"Username": username}, {"$set": {"Retired": True}}, return_document=ReturnDocument.AFTER)
    print(newReview)
    print("Thank you for your service.")

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
        {"_id": "$Status", "count":{"$sum": 1}, "neworder": {"$push": "$order"}},
    },
    {"$sort":
        {"neworder": 1},
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

# review reject ID 1 2 3 4
def reviewManuscript(db, username, input):
    action = None
    manuscript = None
    appropriateness = None
    clarity = None
    methodology = None
    fieldContribution = None
    print(len(input))
    if len(input) != 7:
        print("This review must be formatted like this:\nreview <action> <manuscriptID> <appropriateness> <clarity> <methodology> <fieldContribution>")
        return
    if input[1] == 'accept' or input[1] == 'reject':
        action = input[1]
    else:
        print("The action must be either accept or reject.")
        return
    manuscript = input[2]
    appropriateness = int(input[3])
    clarity = int(input[4])
    methodology = int(input[5])
    fieldContribution = int(input[6])
    if appropriateness not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print("All scores must be whole numbers between 1 and 10.")
        return
    if clarity not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print("All scores must be whole numbers between 1 and 10.")
        return
    if methodology not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print("All scores must be whole numbers between 1 and 10.")
        return
    if fieldContribution not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        print("All scores must be whole numbers between 1 and 10.")
        return
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(timestamp)
    isAssigned = db.Review.find_one({"ManuscriptId": manuscript, "ReviewerUsername": username})
    if isAssigned:
        isUnderReview = db.Manuscript.find_one({"_id": manuscript, "Status": "Under Review"})
        print(isUnderReview)
        if isUnderReview:
            print("doing the review!")
            newReview = db.Review.find_one_and_update({"ManuscriptId": manuscript, "ReviewerUsername": username}, {"$set": {"Appropriateness": appropriateness, "Clarity": clarity, "Methodology": methodology, "ContributionField": fieldContribution, "Recommendation": action, "DateCompleted": timestamp}}, return_document=ReturnDocument.AFTER)
            print(newReview)
        else:
            print("This manuscript is not under review at the moment.")
            return
    else:
        print("You have not been asssigned to review this manuscript.")
        return
