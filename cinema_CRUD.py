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


conn.commit()

cur.close()