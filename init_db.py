import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="learning_platform",
    user=os.environ['DB_USERNAME'],
    password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS courses;')
cur.execute('CREATE TABLE courses (id serial PRIMARY KEY,'
            'title varchar (150) NOT NULL,'
            'review varchar (300) NOT NULL,'
            'text_content text NOT NULL,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
            )

# Insert data into the table

cur.execute('INSERT INTO courses (title, review, text_content)'
            'VALUES (%s, %s, %s)',
            ('A Tale of Two Cities',
             'Charles Dickens',
             'Charles Dickens story about two cites and dickens dick probably',
            )
           )

cur.execute('INSERT INTO courses (title, review, text_content)'
            'VALUES (%s, %s, %s)',
            ('Anna Karenina',
             'Leo Tolstoy',
             'Another great classic!')
            )

conn.commit()

cur.close()
conn.close()
#Hi there