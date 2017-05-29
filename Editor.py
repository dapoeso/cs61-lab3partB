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

def registerEditor(db, input):
    # fill out all of the information
    username = None
    fname = None
    lname = None
    if len(input) == 5:
        username = input[2]
        fname = input[3]
        lname = input[4]
    else:
        print("Please format your query correctly.  You may have included too many or too few fields.\nThe correct format: register editor <username> <firstName> <lastName>")
        return

    # check if the editor username is already in the database; if not, create a new editor
    usernameExists = db.Editor.find_one({"Username": username})
    if usernameExists:
        print("Sorry, but this username has been taken already.  Please try another one.")
        return
    result = db.Editor.insert_one({"Username": username, "FirstName": fname, "LastName": lname})
    print(result.inserted_id)
    test = db.Editor.find_one({"Username": username})
    print(test)

def loginEditor(db, username):
    editorExists = db.Editor.find_one({"Username": username})
    if editorExists:
        firstname = editorExists.get(u'FirstName')
        lastname = editorExists.get(u'LastName')
        print("Hello " + firstname + " " + lastname +"!")
        return True
    else:
        print("Sorry, but this username is invalid.  Please try again or register a new editor.")
        return False

def showEditorStatus(db, username):

    results = db.Manuscript.aggregate([
    {"$lookup":
        {"from": "Editor", "localField": "EditorUsername", "foreignField": "Username", "as": "editor_manuscripts"}
    },
    {"$match":
        {"editor_manuscripts.Username": username}
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

def showEditorStatusList(db, username):

    results = db.Manuscript.aggregate([
    {"$lookup":
        {"from": "Editor", "localField": "EditorUsername", "foreignField": "Username", "as": "editor_manuscripts"}
    },
    {"$match":
        {"editor_manuscripts.Username": username}
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

def assignManuscript(db, username, input):
    if len(input) != 3:
        print("This query is incorrectly formatted.  The form is the following: assign <manuscriptID> <reviewerUsername>")
        return
    manuscript = int(input[1])
    reviewerUsername = input[2]

    # check if editor is assigned manuscript and if it is either under review or received; save the RI code
    isAssigned = db.Manuscript.find_one_and_update({"_id": manuscript, "EditorUsername": username, "Status": {"$in": ["Received", "Under Review"]}}, {"$set": {"Status": "Under Review"}}, return_document=ReturnDocument.AFTER)
    if not isAssigned:
        print("Sorry, but the manuscript is either not assigned to this editor or is not eligible to be under review.")
        return
    RI = int(isAssigned.get(u'RICode'))
    # check if reviewer RI is same as manuscript RI
    interestExists = db.ReviewerInterests.find_one({"ReviewerUsername": reviewerUsername, "RICode": RI})
    if not interestExists:
        print("Sorry, but this reviewer does not have the appropriate field of interest to review this manuscript.")
        return
    # check if reviewer is retired
    reviewerRetired = db.Reviewer.find_one({"Username": reviewerUsername, "Retired": True})
    if reviewerRetired:
        print("Sorry, but the reviewer in question has retired.")
        return
    # check if review has already been assigned
    alreadyReviewing = db.Review.find_one({"ManuscriptId": manuscript, "ReviewerUsername": reviewerUsername})
    if alreadyReviewing:
        print("This reviewer has already been assigned this manuscript.")
        return
    # if this passes all tests, create a new review with null fields
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    newReview = db.Review.insert_one({"ManuscriptId": manuscript, "ReviewerUsername": reviewerUsername, "Appropriateness": None, "Clarity": None, "Methodology": None, "ContributionField": None, "Recommendation": None, "DateSent": timestamp, "DateCompleted": None})
    # print(newReview.inserted_id)

def rejectManuscript(db, username, input):
    if len(input) != 2:
        print("The query must be formatted like this: reject <manuscriptId>")
        return
    manuscript = int(input[1])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    isAssigned = db.Manuscript.find_one_and_update({"_id": manuscript, "EditorUsername": username, "Status": {"$in": ["Received", "Under Review"]}}, {"$set": {"Status": "Rejected", "DateAcceptReject": timestamp}}, return_document=ReturnDocument.AFTER)
    if not isAssigned:
        print("Either the editor does not have the authority to reject this manuscript or the manuscript is beyond rejection.")
        return

def acceptManuscript(db, username, input):
    if len(input) != 2:
        print("The query must be formatted like this: accept <manuscriptId>")
        return
    manuscript = int(input[1])
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    validReviews = db.Review.aggregate([
        {"$match":{"ManuscriptId": manuscript, "DateCompleted": {"$nin":[None]}}},
        { "$group": { "_id": None, "count": { "$sum": 1 } } }
    ])
    if not validReviews:
        print("There have been no reviews completed for this manuscript yet, so it cannot be accepted. A manuscript needs at least 3 reviews to be accepted.")
        return
    count = 0
    for doc in validReviews:
        count = int(doc.get(u'count'))
    if count < 3:
        print("A manuscript must have at least 3 completed reviews before it can be accepted.")
        return
    isAssigned = db.Manuscript.find_one_and_update({"_id": manuscript, "EditorUsername": username, "Status": {"$in": ["Under Review"]}}, {"$set": {"Status": "Accepted", "DateAcceptReject": timestamp}}, return_document=ReturnDocument.AFTER)
    if not isAssigned:
        print("Either the editor does not have the authority to accept this manuscript or the manuscript is past the acceptance phase.")
        return

def typesetManuscript(db, username, input):
    if len(input) != 3:
        print("The query must be formatted like this: typeset <manuscriptId> <pagesOccupied>")
        return
    manuscript = int(input[1])
    pages = int(input[2])
    isAssigned = db.Manuscript.find_one_and_update({"_id": manuscript, "EditorUsername": username, "Status": {"$in": ["Accepted"]}}, {"$set": {"Status": "Typeset", "PagesOccupied": pages}}, return_document=ReturnDocument.AFTER)
    if not isAssigned:
        print("Either the editor does not have the authority to typeset this manuscript or the manuscript not in the appropriate stage to be typeset.")
        return
    # print(isAssigned)

def scheduleManuscript(db, username, input):
    if len(input) != 4:
        print("The query must be formatted like this: schedule <manuscriptId> <year> <period>")
    manuscript = int(input[1])
    year = int(input[2])
    if year < 2017:
        print("Year is too far in the past.  Please use years 2017 and ahead.")
        return
    period = int(input[3])
    if period not in [1, 2, 3, 4]:
        print("Period must be 1, 2, 3, or 4.  Please try again.")
        return
    isAssigned = db.Manuscript.find_one({"_id": manuscript, "EditorUsername": username, "Status": {"$in": ["Typeset"]}})
    if not isAssigned:
        print("Either the editor does not have the authority to schedule this manuscript or the manuscript not in the appropriate stage to be scheduled.")
        return
    manuscriptPages = isAssigned.get(u'PagesOccupied')

    # check if volume exists/has not been published
    journalExists = db.Journal.find_one({"Year": year, "Period": period})
    if journalExists:
        printDate = journalExists.get(u'PrintDate')
        if printDate:
            print("This journal has already been published.")
            return
    else:
        newJournal = db.Journal.insert_one({"Year": year, "Period": period, "PrintDate": None})

    journalManuscripts = db.Manuscript.aggregate([
        {"$match":{"JournalIssueYear": year, "JournalIssuePeriod": period}},
        { "$group": { "_id": None, "totalPages": { "$sum": "$PagesOccupied" } } }
    ])
    # check if adding these pages to volume would exceed 100
    if journalManuscripts:
        totalPages = None
        for doc in journalManuscripts:
            # print(doc)
            totalPages = doc.get(u'totalPages')
            journalPages = totalPages + manuscriptPages
            if journalPages > 100:
                print("Adding in this manuscript would exceed the 100-page limit.")
                return
            else:
                print(journalPages)
    # check if editor is assigned and if it has been typeset
    assignSchedule = db.Manuscript.find_one_and_update({"_id": manuscript, "EditorUsername": username, "Status": {"$in": ["Typeset"]}}, {"$set": {"Status": "Scheduled", "JournalIssueYear": year, "JournalIssuePeriod": period}}, return_document=ReturnDocument.AFTER)
    if assignSchedule:
        print("Scheduled")

def publishJournal(db, input):
    if len(input) != 3:
        print("The query must be formatted like this: publish <year> <period>")
        return
    year = int(input[1])
    period = int(input[2])
    # check if journal exists
    journalExists = db.Journal.find_one({"Year": year, "Period": period, "PrintDate": {"$in": [None]}})
    if not journalExists:
        print("Sorry, but this journal does not seem to exist yet or has already been published.  Please try again.")
        return
    # make sure there is at least 1 manuscript
    manuscriptExists = db.Manuscript.find_one({"JournalIssueYear": year, "JournalIssuePeriod": period})
    if not manuscriptExists:
        print("There are no manuscripts assigned to this journal.  A journal needs at least 1 manuscript for it to be published.")
        return
    # update all of the other manuscripts assigned to this journal
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    publishJournal = db.Journal.find_one_and_update({"Year": year, "Period": period}, {"$set": {"PrintDate": timestamp}}, return_document=ReturnDocument.AFTER)
    # print(publishJournal)
    # for doc in db.Manuscript.find({"JournalIssueYear": year, "JournalIssuePeriod": period, "Status": {"$in": ["Scheduled"]}}):
    #     print(doc)

    result = db.Manuscript.update_many({"JournalIssueYear": year, "JournalIssuePeriod": period, "Status": {"$in": ["Scheduled"]}}, {"$set": {"Status": "Published"}})
    # for doc2 in db.Manuscript.find({"JournalIssueYear": year, "JournalIssuePeriod": period}):
    #     print(doc2)
