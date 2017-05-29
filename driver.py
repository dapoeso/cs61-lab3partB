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


loop = True
while loop:

    textArray = shlex.split(raw_input('Enter a command: '))

    if (textArray[0] == "login"):
        if len(textArray) != 3:
            print("Please login with the following format: login <userType> <username>")
        elif currentUser is not None:
            print("Please logout before you login to another account.")
        elif textArray[1] == "reviewer":
            success = loginReviewer(db, textArray[2])
            # print(success)
            if success:
                currentUser = textArray[2]
                currentUserType = "Reviewer"
                showReviewerStatus(db, currentUser)
        elif textArray[1] == "author":
            print("Logging in author")
            success = loginAuthor(db, textArray[2])
            if success:
                currentUser = textArray[2]
                currentUserType = "Author"
                showAuthorStatus(db, currentUser)
        elif textArray[1] == "editor":
            print("Logging in editor")
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
                showAuthorStatus(db, currentUser)
            elif currentUserType == "Editor":
                showEditorStatus(db, currentUser)
                # print("showing editor status")
        else:
            print("Please log in to see status.")
    if (textArray[0] == "list"):
        if currentUser is not None:
            if currentUserType == "Reviewer":
                showReviewerStatusList(db, currentUser)
            elif currentUserType == "Author":
                showAuthorStatusList(db, currentUser)
            elif currentUserType == "Editor":
                showEditorStatusList(db, currentUser)
                # print("showing editor list")
        else:
            print("Please log in to see status.")


    if (textArray[0] == "assign"):
        if currentUser is not None:
            if currentUserType == "Editor":
                assignManuscript(db, currentUser, textArray)
            else:
                print("You must be an editor to assign a manuscript.")
        else:
            print("Please log in to assign a manuscript.")
    if (textArray[0] == "reject"):
        if currentUser is not None:
            if currentUserType == "Editor":
                rejectManuscript(db, currentUser, textArray)
            else:
                print("You must be an editor to reject a manuscript.")
        else:
            print("Please log in to reject a manuscript.")
    if (textArray[0] == "accept"):
        if currentUser is not None:
            if currentUserType == "Editor":
                acceptManuscript(db, currentUser, textArray)
            else:
                print("You must be an editor to accept a manuscript.")
        else:
            print("Please log in to accept a manuscript.")
    if (textArray[0] == "typeset"):
        if currentUser is not None:
            if currentUserType == "Editor":
                typesetManuscript(db, currentUser, textArray)
            else:
                print("You must be an editor to typeset a manuscript.")
        else:
            print("Please log in to typeset a manuscript.")
    if (textArray[0] == "schedule"):
        if currentUser is not None:
            if currentUserType == "Editor":
                scheduleManuscript(db, currentUser, textArray)
            else:
                print("You must be an editor to schedule a manuscript.")
        else:
            print("Please log in to schedule a manuscript.")
    if (textArray[0] == "publish"):
        if currentUser is not None:
            if currentUserType == "Editor":
                publishJournal(db, textArray)
            else:
                print("You must be an editor to publish a journal.")
        else:
            print("Please log in to publish a journal.")

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


    if (textArray[0] == "submit"):
        if currentUser is not None:
            if currentUserType == "Author":
                submitManuscript(db, currentUser, textArray)
            else:
                print("You must be an author to submit a manuscript.")
        else:
            print("Please log in to submit a manuscript.")
    if (textArray[0] == "retract"):
        if currentUser is not None:
            if currentUserType == "Author":
                retractManuscript(db, currentUser, textArray)
            else:
                print("You must be an author to retract a manuscript.")
        else:
            print("Please log in to retract a manuscript.")

    # REGISTER
    if (textArray[0] == "register" and len(textArray) >= 5):
    	# if(len(textArray) == 8):
    	if (textArray[1] == "author"):
            print("Registering Author . . .")
            registerAuthor(db, textArray)
    	if (textArray[1] == "editor"):
            print("Registering Editor . . .")
            registerEditor(db, textArray)
    	if (textArray[1] == "reviewer"):
            print("Registering Reviewer . . .")
            registerReviewer(db, textArray)
    if (textArray[0] == "logout"):
        if currentUser is not None:
            print("Logging out " + currentUser)
        currentUser = None
        currentUserType = None
    if (textArray[0] == "exit"):
        print("Ok. See you later!")
        loop = False
    if (textArray[0] == "quit"):
        print("Ok. See you later!")
        loop = False
