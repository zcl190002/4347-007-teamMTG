MTG Database Manager

This is a simple database manager for Magic: The Gathering cards.
It's written in Python and uses SQLite3 for the database.
For the GUI, it uses Tkinter and CustomTKinter to give it a more modern look.

Files included:
- MTG.py: The main program file
- MTG.db: The SQLite3 database file

To run the program:
1. Open a terminal or command prompt
2. Make sure you have Python 3.7 or higher installed as well as pip
3. Install the required packages by running the following command:
    'pip install customtkinter pyperclip'
4. Unzip the MTG.zip file
5. Navigate to the unzipped MTG folder in your command prompt
6. Run the program by running the following command in the command prompt:
    'python MTG.py'

Note:
- If you have any issues running the program, please make sure you have
the required packages installed
- If you want to test the update, insert, and delete features,
there are test cards in each table that you can use that are at the bottom
of the table.

Features:
- Search for cards in the database
    - Can dynamically add and remove conditions
    - Can search for cards based on entities such as card name, type_line, power, etc.
    - When searching for numeric values, you can use comparison operators (e.g., >, <, =)
        - For example when using the power condition, entering "> 4" will
        return all cards with power greater than 4
    - Can use conditional operators to filter results (e.g., and, or)
        - Using and will return results that match all conditions,
        while using or will return results that match at least one condition
    - After entering the conditions, hit the "Search" button to start searching and
    the results will be displayed in the table

- Insert new cards into the database
    - Can insert cards at the bottom of the window by entering the card's name,
    type_line, power, toughness, etc. in the text boxes
    - After entering the card information, hit the "Insert" button to insert
    the card(s) into the database
    - The table will automatically update to show all the cards in the database
    including the new card

- Update card information in the database
    - Can update cards in the database using the card's name (primary key)
    - After entering the card's name and the new information, hit the "Update" button
    to update the card's information
    - The table will automatically update to show the updated card

- Delete cards from the database using the card's name
    - Can delete cards from the database using the card's name (primary key)
    - After entering the card's name, hit the "Delete" button to delete the card
    - The table will automatically update
- Quit the program
    - Can quit the program by hitting the "Quit" button

- Different tabs for different MTG table data (e.g., card info, card prices, prints, analytics)
    - Can switch between tabs to view different tables data

Other Features:
- Can copy results to clipboard
- Can export results to txt file
- Can scroll through the table vertically and horizontally to view all results
- Can expand columns to read longer texts



