#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20

@author: Echo, Rachel, Meredith
"""

import sqlite3

conn = sqlite3.connect('cinema.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Movie')
cur.execute('DROP TABLE IF EXISTS Slot')
cur.execute('DROP TABLE IF EXISTS Ticket')
cur.execute('DROP TABLE IF EXISTS User')

# Create

cur.execute('CREATE TABLE Movie (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, genre TEXT)')
cur.execute('CREATE TABLE Slot (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, movie_id INTEGER, time TEXT, isFull INTEGER)')
cur.execute('CREATE TABLE Ticket (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, price DOUBLE, seat INTEGER, slot_id INTEGER, user_id INTEGER)')
cur.execute('CREATE TABLE User (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, email TEXT, password TEXT)')

#Insert

#insert into Slot table
genres = ['Romance', 'Comedy', 'Horror']
movie_dic = {'Romance':['Me Before You', 'Titanic', 'About Time'], 'Comedy':['The Dictator', 'The Gold Rush', 'Four Weddings and a Funeral'], 'Horror':['Silent Hill', 'Saw', 'The Shining']}
slots = ['9:00 - 11:00','13:00 - 15:00','20:00 - 22:00']

#create Movie
for genre_name in genres:
    movies = movie_dic.get(genre_name)
    for movie_name in movies:
        params = (movie_name, genre_name)
        # print(params)
        cur.execute('INSERT INTO Movie (name, genre) values (?, ?)', (movie_name, genre_name))

#create Slot
for movie_id in range(1,10):
    for slot in slots:
        cur.execute('INSERT INTO Slot (movie_id, time, isFull) values (?, ?, ?)', (movie_id, slot, 0))

# Ticket Insert on purchase

# User Insert on sign up
cur.execute("INSERT INTO User (email, password) values ('kwin1994@gmail.com', 'kwin1994')")
cur.execute("INSERT INTO User (email, password) values ('katto1996@gmail.com', 'katto1996')")
cur.execute("INSERT INTO User (email, password) values ('messi1987@gmail.com', 'messi1987')")

#specify the values as question marks (?, ?)
# to indicate that the actual values are passed in 
# #as a tuple ( 'My Way', 15 ) as the second parameter to the execute() call
# cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)',
#     ('Thunderstruck', 20))
# cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)',
#     ('My Way', 15))


# # The INSERT statement implicitly opens a transaction,
# # which needs to be committed before changes are saved in the database 
# #call conn.commit() on the connection object to commit the transaction
# conn.commit()


# print('Tracks:') 
# cur.execute('SELECT title, plays FROM Tracks') # retrieve the rows from the table

# #the cursor is something we can loop through in a for statement
# # For efficiency, the cursor does not read all of the data from the database 
# #when we execute the SELECT statement. Instead, the data is read on demand 
# #as we loop through the rows in the for statement.
# for row in cur: 
#      print(row)

# #After the DELETE is performed,
# # call commit() to force the data to be removed from the database
# cur.execute('DELETE FROM Tracks WHERE plays < 100')
conn.commit()

cur.close()