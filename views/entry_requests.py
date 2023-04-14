import sqlite3
import json
from modals import Entry, Mood, Tag, TagId
from .tag_requests import get_single_tag

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT DISTINCT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            m.label mood_label,
            e.date,
            (
           SELECT GROUP_CONCAT(t.id)
            FROM EntryTags et
            JOIN Tags t ON et.tag_id = t.id
            WHERE et.entry_id = e.id) as tag_id
            FROM Entry e
            JOIN Mood m
                ON m.id = e.mood_id
            LEFT OUTER JOIN EntryTags et
                    ON e.id = et.entry_id
            LEFT OUTER JOIN Tags t
                    ON et.tag_id = t.id
        """)
        # Initialize an empty list to hold all animal representations
        entries = []
        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()
        # Iterate list of data returned from database
        for row in dataset:
            # Create an animal instance from the current row
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'], row['date'])
            mood = Mood(row['mood_id'], row['mood_label'])
            #tag = Tag(row['tag_id'], row['subject'])
            # Add the dictionary representation of the animal to the list
            entry.mood = mood.__dict__

            tag_ids = row['tag_id'].split(',') if row['tag_id'] else []
            tags = []
            for tag_id in tag_ids:
               tag_object = get_single_tag(tag_id)
               tags.append(tag_object)
            entry.tags = tags
            entries.append(entry.__dict__)

    return entries
def get_enteries_by_search(query):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM Entry e
        WHERE e.entry LIKE ?
        """, ( f"%{query}%", ))

        enteries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            enteries.append(entry.__dict__)

    return enteries

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM Entry e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'], data['mood_id'],
                            data['date'])

    return entry.__dict__
    
def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))

def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT * 
            FROM Entry
            LEFT OUTER JOIN EntryTags 
                ON Entry.id = EntryTags.entry_id
            LEFT OUTER JOIN Tags
                ON EntryTags.tag_id = Tags.id
        """)
        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, entry, mood_id, date )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['mood_id'], new_entry['date'], ))
        id = db_cursor.lastrowid
        new_entry['id'] = id
        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO EntryTags
                (entry_id, tag_id)
            VALUES
                (?, ?)
            """, (new_entry['id'], tag, ))

    return new_entry

def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['mood_id'], new_entry['date'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True