import sqlite3
import json
from modals import Mood

def get_all_moods():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Mood m
        """)

        # Initialize an empty list to hold all animal representations
        moods = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            mood = Mood(row['id'], row['label'])

            # Create a Location instance from the current row
        

            # Add the dictionary representation of the location to the animal
           

            # Add the dictionary representation of the animal to the list
            moods.append(mood.__dict__)

    return moods

def get_single_mood(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Mood m
        WHERE m.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        mood = Mood(data['id'], data['label'])

    return mood.__dict__