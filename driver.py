from pymongo import MongoClient
import shlex
from Author import *
from Reviewer import *
from Editor import *
import sys


# client = MongoClient()

client = MongoClient("mongodb://Team11:zuqXM5saOsbd4DOr@cluster0-shard-00-00-ppp7l.mongodb.net:27017,cluster0-shard-00-01-ppp7l.mongodb.net:27017,cluster0-shard-00-02-ppp7l.mongodb.net:27017/Team11DB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")

db = client.Team11DB
currentUser = None
currentUserType = None

# cursor = db.Author.find()

# for document in cursor:
#     print(document)
loop = True
while loop:
    textArray = shlex.split(raw_input('Enter a command: '))
    # print()
    # print(textArray)
    # print()
    if (textArray[0] == "login"):
        if len(textArray) != 3:
            print("Please login with the following format: login <userType> <username>")
        elif textArray[1] == "reviewer":
            success = loginReviewer(db, textArray[2])
            # print(success)
            if success:
                currentUser = textArray[2]
                currentUserType = "Reviewer"
                showReviewerStatus(db, currentUser)
        elif textArray[1] == "author":
            print("Logging in author")
        elif textArray[1] == "editor":
            print("Loggin in editor")
            success = loginEditor(db, textArray[2])
            # print(success)
            if success:
                currentUser = textArray[2]
                currentUserType = "Editor"
                showEditorStatus(db, currentUser)

    if (textArray[0] == "status"):
        if currentUser is not None:
            if currentUserType == "Reviewer":
                showReviewerStatus(db, currentUser)
            elif currentUserType == "Author":
                print("showing author status")
            elif currentUserType == "Editor":
                showEditorStatus(db, currentUser)
                print("showing editor status")
        else:
            print("Please log in to see status.")
    if (textArray[0] == "list"):
        if currentUser is not None:
            if currentUserType == "Reviewer":
                showReviewerStatusList(db, currentUser)
            elif currentUserType == "Author":
                print("showing author list")
            elif currentUserType == "Editor":
                showEditorStatusList(db, currentUser)
                print("showing editor list")
        else:
            print("Please log in to see status.")
    if (textArray[0] == "review"):
        if currentUser is not None:
            if currentUserType == "Reviewer":
                reviewManuscript(db, currentUser, textArray)
            else:
                print("You must be a reviewer to review a manuscript.")
        else:
            print("Please log in to review a manuscript.")
    if (textArray[0] == "retire"):
        if currentUser is not None and currentUserType == "Reviewer":
            retireReviewer(db, currentUser)
            currentUser = None
            currentUserType = None
        else:
            print("Sorry, but you are either not logged in or a reviewer.")
    # REGISTER
    if (textArray[0] == "register" and len(textArray) >= 5):
    	# if(len(textArray) == 8):
    	if (textArray[1] == "author"):
            print("Registering Author . . .")
    		# registerAuthor(db, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], textArray[7])
            # showAuthorStatus(db, textArray[2])
    	# register|editor|fname|lname
    	if (textArray[1] == "editor"):
            print("Registering Editor . . .")
            registerEditor(db, textArray)
    		# registerEditor(collection, textArray[2], textArray[3], PASSWORD)

    	# register|reviewer|fname|lname|email|affiliation|one|two|three
    	if (textArray[1] == "reviewer"):
            print("Registering Reviewer . . .")
            registerReviewer(db, textArray)
    		# else:
			# 	print("ERROR: Must register reviewer with 1-3 RI Codes")
    if (textArray[0] == "logout"):
        print("Logging out " + currentUser)
        currentUser = None
        currentUserType = None
    if (textArray[0] == "exit"):
        print("Ok. See you later!")
        loop = False
    if (textArray[0] == "quit"):
        print("Ok. See you later!")
        loop = False
