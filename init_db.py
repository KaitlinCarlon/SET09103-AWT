import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
                connection.executescript(f.read())

                cur = connection.cursor()

                cur.execute("INSERT INTO entries (entry_title, content, feeling_rating, greatful) VALUES (?, ?, ?, ?)",
                                    ('First Post', 'Content for the first post', '4', 'my dog')
                                                )

                cur.execute("INSERT INTO entries (entry_title, content, feeling_rating, greatful) VALUES (?, ?, ?, ?)",
                                    ('Second Post', 'Content for the second post', '8', 'coffee')
                                                )

                connection.commit()
                connection.close()
