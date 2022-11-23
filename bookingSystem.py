import sqlite3
import time
import timeout_decorator

#global variables
price = 14.99
# is_logged_in = False



@timeout_decorator.timeout(60*5)
def booking():

    is_logged_in = False
    #Welcome
    print("\n********************WELCOME TO LALALAND MOVIE BOOKING TICKET SYSTEM***********************")

    while True:

        #Sign up / in
        print("\n********************WELCOME TO SIGNUP/IN PAGE***********************")
        print("\nPlease enter your email address and password; if you don't have an account with us, we will automatically create one for you ^_^")

        email_input = ''

        while is_logged_in == False:

            email_input = input("\nPlease enter your email address: ")

            cur.execute('SELECT * FROM User WHERE email = ? ', (email_input, ))
            user_found = cur.fetchone()

            #If there's no such user, we just create a new one
            if user_found == None: 
                password = input("\nPlease set up your password: ")
                cur.execute('INSERT INTO User (email, password) values (?, ?)', (email_input, password))
                conn.commit()
                is_logged_in = True
                print("\n------------A new account has been created!------------")
            #If the user exists
            else:
                password = input("\nPlease enter your password:")
                password_found = user_found[2]
                #If the password is correct
                if password == password_found:
                    is_logged_in = True
                    print("\n-----------Logged in successfully!-----------")
                #Otherwise
                else:
                    print("Wrong password! Please try again!")

        while is_logged_in == True:
            
            cur.execute('SELECT id FROM User WHERE email = ?', (email_input,))
            user_id = cur.fetchone()[0]

        #Three options
            print("\n-----------What would you like to do? Please enter the number:-----------")
            print("\n1. BUY TICKETS")
            print("\n2. VIEW PURCHASED TICKETS")
            print("\n3. LOG OUT")
            while True:
                choice = int(input("\n"))
                if choice in range(1, 4):
                    break
                else:
                    print("\n Input not in range 1-3, please try again!")

            if choice == 1:

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
                seats = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                capacity = len(seats)
                cur.execute('SELECT * FROM Slot WHERE movie_id = ? AND time = ?', (movie_id, time_chosen))
                slot_id = cur.fetchone()[0]
                cur.execute('SELECT * FROM Ticket WHERE slot_id = ?', (slot_id,))
                tickets = cur.fetchall()
                # remove seats that have been sold in this slot
                if tickets != None:
                    for ticket in tickets:
                        seats.remove(ticket[2])
                print("\n-----------Please choose a preferred seat from below:-----------")
                for seat in seats:
                    print('\n', seat)
                while True:
                    seat_chosen = input("\n Please enter your chosen Seat: ")
                    try:
                        seat_chosen = int(seat_chosen)
                        if seat_chosen in seats:
                            break
                        else:
                            print("\n Wrong seat, please try again")
                    except:
                        print("\n Please enter a number from available seats above")

                # Insert a new ticket and print detailed information
                # cur.execute('SELECT id FROM User WHERE email = ?', (email_input,))
                # user_id = cur.fetchone()[0]
                cur.execute("INSERT INTO Ticket (price, seat, slot_id, user_id) values (?, ?, ?, ?)", (price, seat_chosen, slot_id, user_id))
                conn.commit()
                print("\n-----------Below is the detailed information of the ticket you purchased:-----------")
                print("\n Movie: ", movie_chosen)
                print("\n Slot: ", time_chosen)
                print("\n Seat: ", seat_chosen)
                print("\n Price: $", price)

                #Check if a slot is full
                cur.execute('SELECT * FROM Ticket WHERE slot_id = ?', (slot_id,))
                ordered_tickets = cur.fetchall()
                print(len(ordered_tickets))
                if len(ordered_tickets) == capacity:
                    cur.execute('UPDATE Slot set isFull = 1 where id = ?', (slot_id,))
                    conn.commit()
            
            elif choice == 2:
                #View tickets bought
                tickets_purchased = cur.execute('SELECT * FROM Ticket WHERE user_id = ?', (user_id,)).fetchall()
            
                print("\nBelow are your purchased tickets:")
                for i in range(len(tickets_purchased)):
                    # get slot
                    cur.execute('SELECT * FROM Slot WHERE id = ?', (tickets_purchased[i][3],))
                    slot_purchased = cur.fetchone()
                    movie_id_purchased = slot_purchased[1]
                    time_purchased = slot_purchased[2]

                    cur.execute('SELECT name FROM Movie WHERE id = ?', (movie_id_purchased,))
                    movie_purchased = cur.fetchone()[0]

                    print("\n -----Ticket %d-----"%(i + 1))
                    print("\n Movie: ", movie_purchased)
                    print("\n Slot: ", time_purchased)
                    print("\n Seat: ", tickets_purchased[i][2])
                    print("\n Price: $14.99")
        
            else:
                is_logged_in = False
            
            conn.commit()
        

if __name__ == '__main__':

    conn = sqlite3.connect('cinema.sqlite')
    cur = conn.cursor()

    try:
        booking()
    except Exception as e:
        print ('\n Your session has timed out, please try again!')


    # close database upon time out
    conn.close()
