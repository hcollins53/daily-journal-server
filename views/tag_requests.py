import sqlite3
import json
from modals import Tag

def get_all_tags():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            t.id,
            t.subject
        FROM Tags t
        """)
        # Initialize an empty list to hold all animal representations
        tags = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create an animal instance from the current row
            tag = Tag(row['id'], row['subject'])
            # Add the dictionary representation of the animal to the list_
            tags.append(tag.__dict__)

    return tags

def get_single_tag(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            t.id,
            t.subject
        FROM Tags t
        WHERE t.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        tag = Tag(data['id'], data['subject'])

    return tag.__dict__