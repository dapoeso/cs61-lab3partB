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
    else:
        print("Yay!")
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
    },
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
    # check if editor is assigned manuscript and if it is either under review or received; save the RI code
    # check if reviewer is retired
    # check if reviewer RI is same as manuscript RI
    # if they match, create a new review with null fields
