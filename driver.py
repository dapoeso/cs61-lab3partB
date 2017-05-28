from pymongo import MongoClient
import shlex
from Author import *
from Reviewer import *
import sys


# client = MongoClient()

client = MongoClient("mongodb://Team11:zuqXM5saOsbd4DOr@cluster0-shard-00-00-ppp7l.mongodb.net:27017,cluster0-shard-00-01-ppp7l.mongodb.net:27017,cluster0-shard-00-02-ppp7l.mongodb.net:27017/Team11DB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")

db = client.Team11DB
currentUser = "reaganmcknight"

# cursor = db.Author.find()

# for document in cursor:
#     print(document)
loop = True
while loop:
    # print()
    # text = shlex.split(raw_input('Enter a command: '))
    # textArray = text.split('|')
    textArray = shlex.split(raw_input('Enter a command: '))
    # print()
    # print(textArray)
    # print()
    if (textArray[0] == "show"):
        showReviewerStatusList(db, currentUser)
    # REGISTER
    if (textArray[0] == "register"):
    	# if(len(textArray) == 8):
    	if (textArray[1] == "author"):
            print("Registering Author . . .")
    		# registerAuthor(db, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], textArray[7])
            # showAuthorStatus(db, textArray[2])
    	# register|editor|fname|lname
    	if (textArray[1] == "editor"):
            print("Registering Editor . . .")
    		# registerEditor(collection, textArray[2], textArray[3], PASSWORD)

    	# register|reviewer|fname|lname|email|affiliation|one|two|three
    	if (textArray[1] == "reviewer"):
            print("Registering Reviewer . . .")
    		# if (len(textArray) == 7):
    		# 	print("Registering Reviewer . . .")
    		# 	# registerReviewerWithOne(collection, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], PASSWORD)
    		# elif (len(textArray) == 8):
    		# 	print("Registering Reviewer . . .")
    		# 	# registerReviewerWithTwo(collection, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], textArray[7], PASSWORD)
    		# elif (len(textArray) == 9):
    		# 	print("Registering Reviewer . . .")
    		# 	# registerReviewerWithThree(collection, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], textArray[7], textArray[8], PASSWORD)
            registerReviewer(db, textArray)
    		# else:
			# 	print("ERROR: Must register reviewer with 1-3 RI Codes")
    if (textArray[0] == "exit"):
        print("Ok. See you later!")
        loop = False
    if (textArray[0] == "quit"):
        print("Ok. See you later!")
        loop = False
