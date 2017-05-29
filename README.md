# CS61: Lab 3, Part B

### Setup
Before running, please go to the CS61Lab3PartA folder and install the packages using: ```npm install```


To set up the tables, in the CS61Lab3PartA folder, please start with the following command: ```node MMSetup.js```


This command will set up all of the files in our database and insert some basic data for testing.


Now, please ```cd ..``` to go to the outer directory.


### Functionalities
QUIT: A user may quit out of the program at any time using the following command:


```quit```


#### Author functionality:


REGISTER: A user may register an author using the following command:


```register author [username] [fname] [lname] [email] “[mailing address]” "[affiliation]"```


LOGIN: A user may login to an author account using the following command:


```login author [username]```


This will also be followed by the output from the "Status" command.


STATUS: A user may show the status of his or her author account, which will provide a summary of the number of manuscripts in various phases. Please note that using the "List" command will show specific information about manuscripts with which the author is associated as a primary author. An author may see status using the following command:


```status```


LIST: This command shows specific information about the manuscripts with which the author is associated as a primary author. An author may see his or her list of manuscripts using the following command:


```list```


SUBMIT: This command allows authors to submit manuscripts for which he or she is the primary author. This command provides the title, the author's current affiliation (a string), RICode representing the subject area, optional additional authors, and the document itself (we made this a string as per our discussion in class). The author affiliation will be updated to reflect the affiliation in this manuscript.  An author may submit a manuscript with the following command:


```submit [title] [affiliation] [RICode] [author2] [author3] [author4] [documentString]```


RETRACT: This command allows authors to retract a manuscript from the system. This command asks if the author is sure.  If the answer is yes, then the reviews and manuscript will be retracted from the system. An author may retract a manuscript with the following command:


```retract [manuscriptID]```


#### Editor functionality:


REGISTER: A user may register an editor using the following command:


```register editor [username] [fname] [lname]```


LOGIN: A user may login to an editor account using the following command:


```login author [username]```


This will also be followed by the output from the "Status" command.


STATUS: A user may show the status of his or her editor account, which will provide a summary of the number of manuscripts in various phases. Please note that using the "List" command will show specific information about manuscripts with which the editor is associated. An editor may see status using the following command:


```status```


LIST: This command shows specific information about the manuscripts with which the editor is associated. An editor may see his or her list of manuscripts using the following command:


```list```

ASSIGN: This command assigns a manuscript to a reviewer to be reviewed.  This command ensures that the editor has the authority to assign the manuscript, that the reviewer is not retired, that the manuscript is not already published/typeset, and that the reviewer has an interest in the field of the manuscript.  This creates a blank review for the reviewer that the reviewer may fill out at his or her discretion.  An editor may assign a manuscript for review using the following command:


```assign [manuscriptID] [reviewerUsername]```


REJECT: This command sets the status of a manuscript to "Rejected."  This command ensures that the editor has the authority to reject the manuscript and that the manuscript is in a stage that allows it to be rejected.  Then, this command marks the time that the decision was made and sets the status of the manuscript to "Rejected."  An editor may reject a manuscript with the following command:


```reject [manuscriptID]```


ACCEPT: This command sets the status of a manuscript to "Accepted."  This command ensures that the editor has the authority to accept the manuscript, that the manuscript is in the appropriate stage to be accepted and that the manuscript has at least 3 completed reviews associated with it.  Then, the command marks that time that the decision was made and sets the status of the manuscript to "Accepted.""  An editor may accept a manuscript with the following command:


```accept [manuscriptID]```


TYPESET: This command sets the status of a manuscript to "Typeset."  This command ensures that the editor has the authority to typeset the manuscript and that the manuscript is in the appropriate stage to be typeset.  Then, the command updates the status to "Typeset" and stores the number of pages that the manuscript will occupy.  An editor may typeset a manuscript with the following command:


```typeset [manuscriptID] [pagesOccupied]```


SCHEDULE: This command sets the status of a manuscript to "Scheduled" and assigns it to the appropriate issue.  This command ensures that the year and issue number the editor enters are valid (no past years, no invalid issue numbers), that the editor has the authority to schedule the manuscript, that the manuscript is in the appropriate stage to be scheduled (typeset), that the issue in question has not already been published, that the issue in question exists (if not, then it is created) and that adding the manuscript would not exceed the 100-page limit per issue.  Then, the command updates the status of the manuscript to "Scheduled" and updates the issue number and year.  Unlike the command provided to us in the spec, we decided to implement this by dividing issue into its components, year and period, on the command line.  An editor may schedule a manuscript with the following command:


```schedule [manuscriptID] [Year] [Period]```


PUBLISH: This command publishes an issue and sets the status of all its manuscripts to "Published."  This command ensures that the issue exists, that it has not already been published and that the issue contains at least 1 manuscript.  Then, the command updates the print date (assumed to be the date/time that the publish decision is made because this causes the issue to be sent for publication) and updates the status of all of the manuscripts in the issue to "Published."  An editor may publish an issue with the following command:


```publish [Year] [Period]```


#### Reviewer functionality:


REGISTER: This command registers a reviewer.  We collect information about a reviewer's affiliation and email because this is one of the only opportunities to do so.  This command also assumed that users are not retired upon registration.  A user may register a reviewer using the following command:


```register reviewer [username] [fname] [lname] [email] "[affiliation]" [RICode1] [RICode2] [RICode3] ```


RESIGN: This command resigns a reviewer.  This command updates the Retired field of a user, and thanks the user, and logs out the user.  The reviews that a resigned reviewer has not completed will not appear in the tallies for valid reviews to determine manuscript approval.  In addition, the user will not be able to login after resigning.  A reviewer may resign using the following command:


```resign```


LOGIN: A user may login to a reviewer account using the following command:


```login reviewer [reviewerUsername]```


This will also be followed by the output from the "Status" command.


STATUS: A user may show the status of his or her reviewer account, which will provide a summary of the number of manuscripts in various phases associated with the reivewer. Please note that using the "List" command will show specific information about manuscripts with which the reviewer is associated. A reviewer may see status using the following command:


```status```


LIST: This command shows specific information about the manuscripts with which the reviewer is associated. A reviewer may see his or her list of manuscripts using the following command:


```list```


REVIEW: This command allows a reviewer to submit a review about a specific manuscript.  This command checks that the reviewer has the authority to review the manuscript and that the manuscript is under review.  The manuscript records the timestamp of the recommendation(accept/reject) and notes all the scores in the review table.  We designed this command so that a reviewer may revise his or her review.  A reviewer may review a manuscript with the following command:


```review [recommendation] [manuscriptID] [appropriateness] [clarity] [methodology] [contributionToField]```
