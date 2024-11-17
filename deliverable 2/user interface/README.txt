#	MTG Database Manager

This is a simple database manager for Magic: The Gathering cards.
It's written in Python and uses SQLite3 for the database.
For the GUI, it uses Tkinter and CustomTKinter to give it a more modern look.

Files included:
-	MTG.py: The main program file
-	MTG.db: The SQLite3 database file



#	Running the program

1.	Clone this repo and unzip if necessary
2.	Make sure you have Python 3.7 and pip installed
3.	Install the required packages by running the following command:
	-	'pip install customtkinter pyperclip'
4.	Navigate to the directory containing MTG.db and MTG.py
5.	Run the program using the following command:
	-	`python MTG.py` or `python3 MTG.py` 

Video of program running locally on our machine is attached to the eLearning submission.

Side Notes:
-	If you have any issues running the program, please make sure you have
	the required packages installed
-	If you want to test the update, insert, and delete features,
	there are test cards in each table that you can use that are at the bottom
	of the table.



#	Key Features:

1.	SEARCH FOR CARDS IN THE DATABASE
    -	Can dynamically add and remove conditions
    -	Can search for cards based on entities such as card name, type_line, power, etc.
    -	When searching for numeric values, you can use comparison operators (e.g., >, <, =)
        -	For example when using the power condition, entering "> 4" will
        -	return all cards with power greater than 4
    -	Can use conditional operators to filter results (e.g., and, or)
        -	Using and will return results that match all conditions,
        -	while using or will return results that match at least one condition
    -	After entering the conditions, hit the "Search" button to start searching and
    -	the results will be displayed in the table

2.	INSERT NEW CARDS INTO THE DATABASE
    -	Can insert cards at the bottom of the window by entering the card's name,
    -	type_line, power, toughness, etc. in the text boxes
    -	After entering the card information, hit the "Insert" button to insert
    -	the card(s) into the database
    -	The table will automatically update to show all the cards in the database
    -	including the new card

3.	UPDATE CARD INFORMATION IN THE DATABASE
    -	Can update cards in the database using the card's name (primary key)
    -	After entering the card's name and the new information, hit the "Update" button
    -	to update the card's information
    -	The table will automatically update to show the updated card

4.	DELETE CARDS FROM THE DATABASE USING THE CARD'S NAME
    -	Can delete cards from the database using the card's name (primary key)
    -	After entering the card's name, hit the "Delete" button to delete the card
    -	The table will automatically update

5.	QUIT THE PROGRAM
    -	Can quit the program by hitting the "Quit" button

6.	DIFFERENT TABS FOR DIFFERENT MTG TABLE DATA (E.G., CARD INFO, CARD PRICES, PRINTS, ANALYTICS)
    -	Can switch between tabs to view different tables data

7.	OTHER FEATURES:
	-	Can copy results to clipboard
	-	Can export results to txt file
	-	Can scroll through the table vertically and horizontally to view all results
	-	Can expand columns to read longer texts
