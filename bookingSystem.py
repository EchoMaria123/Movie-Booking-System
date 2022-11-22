import sqlite3

conn = sqlite3.connect('cinema.sqlite')
cur = conn.cursor()

is_logged_in = False

#Welcome
print("\n********************WELCOME TO LALALAND MOVIE BOOKING TICKET SYSTEM***********************")
#Sign up / in
print("\n Please enter your email address and password; if you don't have an account with us, we will automatically create one for you ^_^")

while (is_logged_in == False):

    email_input = input("\nPlease enter your email address: ")

    cur.execute('SELECT * FROM User WHERE email = ? ', (email_input, ))
    user_found = cur.fetchone()

    #If there's no such user, we just create a new one
    if (user_found == None): 
        password = input("\nPlease set up your password: ")
        cur.execute('INSERT INTO User (email, password) values (?, ?)', (email_input, password))
        is_logged_in = True
        print("\n------------A new account has been created!------------")
    #If the user exists
    else:
        password = input("\nPlease enter your password:")
        password_found = user_found[2]
        #If the password is correct
        if (password == password_found):
            is_logged_in = True
            print("\n-----------Logged in successfully!-----------")
        #Otherwise
        else:
            print("Wrong password! Please try again!")

#Buy tickets
print("\n-----------Now time to book tickets!-----------")
    
genres = ['Romance', 'Comedy', 'Horror']
#Return all genres
print("\n-----------Please choose a preferred Genre from below:-----------")
for genre in genres:
    print("\n ", genre)
while True:
    genre_chosen = input("\n Please enter your chosen Genre: ")
    if genre_chosen in genres:
        break
    else:
        print("\n Wrong genre, please try again")

#Return all movies
movie_dic = {'Romance':['Me Before You', 'Titanic', 'About Time'], 'Comedy':['The Dictator', 'The Gold Rush', 'Four Weddings and a Funeral'], 'Horror':['Silent Hill', 'Saw', 'The Shining']}
movies = movie_dic.get(genre_chosen)
print("\n-----------Please choose a preferred Movie from below:-----------")
for movie in movies:
    print('\n', movie)
while True:
    movie_chosen = input("\n Please enter your chosen Movie: ")
    if movie_chosen in movies:
        break
    else:
        print("\n Wrong movie, please try again")

#Return all available slots (isFull = 0)

#get movie id
cur.execute('SELECT id FROM Movie WHERE name = ? ', (movie_chosen, ))
movie_id = cur.fetchone()[0]
#get available slots
cur.execute('SELECT * FROM Slot WHERE movie_id = ? AND isFull = 0', (movie_id, ))
slots_available = cur.fetchall()
times = []
print("\n-----------Please choose a preferred time slot from below:-----------")
for slot_available in slots_available:
    times.append(slot_available[2])
    print('\n', slot_available[2])
while True:
    time_chosen = input("\n Please enter your chosen time slot: ")
    if time_chosen in times:
        break
    else:
        print("\n Wrong time slot, please try again")


#Return all seats available
#User select 
    #If the entered seat is not available, print something (this could be omitted if we assume every input is valid)
    #Otherwise, insert a new ticket and print detailed information
        #If SELECT count (*) from Ticket WHERE slot_id = XXXX is 9, 
        #UPDATE Slot SET isFull = 1 WHERE id = XXXXX

#View tickets bought



conn.commit()

cur.close()