import re
import sqlite3
import time
import timeout_decorator
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


#global variables
PRICE = 14.99
GENRES = ['Romance', 'Comedy', 'Horror']
MOVIE_DIC = {'Romance':['Me Before You', 'Titanic', 'About Time'], 'Comedy':['The Dictator', 'The Gold Rush', 'Four Weddings and a Funeral'], 'Horror':['Silent Hill', 'Saw', 'The Shining']}
TOTAL_SEATS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
CAPACITY = len(TOTAL_SEATS)

#The sender mail addresses and password
SENDER_ADDRESS = 'lalalandmoviebooking@gmail.com'
SENDER_PASSWORD = 'qcxzmejemoragvav'
EMAIL_SUBJECT = 'Congratulations! You have successfully purchased a ticket from LALALAND!'

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Define a function 
# for validating an Email
def check(email):

	# pass the regular expression
	# and the string into the fullmatch() method
	if (re.fullmatch(regex, email)):
		return True
	else:
		return False


def send_mail(receiver_address, movie_chosen, time_chosen, seat_chosen):
    mail_content = '''Dear Customer,\n\nCongratulations on successfully purchasing a ticket from LaLaLand Movie Booking System! Below is the detailed information of your ticket:\n\nMovie: %s\nSlot: %s\nSeat: %s\nPrice: $%.2f\n\nThank You,\nLaLaLand Movie Booking Team
    '''%(movie_chosen, time_chosen, seat_chosen, PRICE)

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = SENDER_ADDRESS
    message['To'] = receiver_address
    message['Subject'] = EMAIL_SUBJECT   #The subject line

    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port, aka connecting to the server
    session.starttls() #enable security
    session.login(SENDER_ADDRESS, SENDER_PASSWORD) #login with mail_id and password to the server
    text = message.as_string() #the MIMEMultipart object has to be converted to a string to be sent
    session.sendmail(SENDER_ADDRESS, receiver_address, text)
    session.quit() #log out of the server

#session time limit 10 minutes
#add time out session to ensure database is closed eventually
@timeout_decorator.timeout(600)
def booking():

    is_logged_in = False
    #Welcome
    print("\n********************WELCOME TO LALALAND MOVIE BOOKING TICKET SYSTEM***********************")

    while True:

        #Sign up / in
        print("\n********************WELCOME TO SIGNUP/SIGNIN PAGE***********************")
        print("\nPlease enter your email address and password; if you don't have an account with us, we will automatically create one for you ^_^")

        email_input = ''

        while is_logged_in == False:

            while True:
                #whether it is a valid email
                email_input = input("\nPlease enter your email address: ")

                #old way for validating email: use api
                # response = requests.get("https://isitarealemail.com/api/email/validate", params = {'email': email_input})
                # status = response.json()['status']

                #revised way: use regular expression
                #limitation: can only be used to check email format, can not check for existence of email
                is_valid_email = check(email_input)

                if is_valid_email == True:
                    break
                else:
                    print('\nThe email you input does not exist or is unknown, please enter again!')

            cur.execute('SELECT * FROM User WHERE email = ? ', (email_input,))
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
                    print("\nWrong password! Please try again!")

        while is_logged_in == True:
            
            cur.execute('SELECT id FROM User WHERE email = ?', (email_input,))
            user_id = cur.fetchone()[0]

        #Three options
            print("\n-----------What would you like to do? Please enter the number:-----------")
            print("\n1. BUY TICKETS")
            print("\n2. VIEW PURCHASED TICKETS")
            print("\n3. LOG OUT")
            while True:
                choice = input("\nYou choose: ")
                try:
                    choice = int(choice)
                    if choice in range(1, 4):
                        break
                    else:
                        print("\nWrong choice, please try again")
                except Exception as e:
                    # print(e)
                    print("\nPlease enter a number from available choices above")

            if choice == 1:

                #Buy tickets
                print("\n-----------Now time to book tickets!-----------")
                
                #Return all genres
                print("\n-----------Please choose a preferred Genre from below:-----------")
                for i in range(len(GENRES)):
                    print("\n%d. %s"%(i + 1, GENRES[i]))
                while True:
                    genre_idx = input("\nPlease enter your chosen Genre: ")
                    try:
                        genre_idx = int(genre_idx)
                        if genre_idx in range(1, len(GENRES) + 1):
                            break
                        else:
                            print("\nWrong genre, please try again")
                    except:
                        print("\nPlease enter a number from available genres above")
                genre_chosen = GENRES[genre_idx - 1]

                #Return all movies
                movies = MOVIE_DIC.get(genre_chosen)
                print("\n-----------Please choose a preferred Movie from below:-----------")
                for i in range(len(movies)):
                    print("\n%d. %s"%(i + 1, movies[i]))
                while True:
                    movie_idx = input("\nPlease enter your chosen Movie: ")
                    try:
                        movie_idx = int(movie_idx)
                        if movie_idx in range(1, len(movies) + 1):
                            break
                        else:
                            print("\nWrong movie, please try again")
                    except:
                        print("\nPlease enter a number from available movies above")
                movie_chosen = movies[movie_idx - 1]

                #Return all available slots (isFull = 0)

                #get movie id
                cur.execute('SELECT id FROM Movie WHERE name = ? ', (movie_chosen,))
                movie_id = cur.fetchone()[0]
                #get available slots
                cur.execute('SELECT * FROM Slot WHERE movie_id = ? AND isFull = 0', (movie_id,))
                slots_available = cur.fetchall()
                #get available times 
                times = []
                print("\n-----------Please choose a preferred time slot from below:-----------")
                for i in range(len(slots_available)):
                    times.append(slots_available[i][2])
                    print("\n%d. %s"%(i + 1, slots_available[i][2]))
                while True:
                    time_idx = input("\nPlease enter your chosen Slot: ")
                    try:
                        time_idx = int(time_idx)
                        if time_idx in range(1, len(times) + 1):
                            break
                        else:
                            print("\nWrong slot, please try again")
                    except:
                        print("\nPlease enter a number from available slots above")
                time_chosen = times[time_idx - 1]

                #Return all seats available
                seats = TOTAL_SEATS
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
                    seat_chosen = input("\nPlease enter your chosen Seat: ")
                    try:
                        seat_chosen = int(seat_chosen)
                        if seat_chosen in seats:
                            break
                        else:
                            print("\nWrong seat, please try again")
                    except:
                        print("\nPlease enter a number from available seats above")

                confirmation = input("\n-----------Please enter y to confirm purchase. Otherwise, please press any other key.-----------\n")
                if confirmation == 'y' or confirmation == 'Y':
                    # Insert a new ticket and print detailed information
                    cur.execute("INSERT INTO Ticket (price, seat, slot_id, user_id) values (?, ?, ?, ?)", (PRICE, seat_chosen, slot_id, user_id))
                    conn.commit()

                    #send confirmation email 
                    send_mail(email_input, movie_chosen, time_chosen, seat_chosen)
                    print("\n-----------Order confirmed. A confirmation email has been sent to your email account %s.-----------"%(email_input))
                    print("\n-----------Below is the detailed information of the ticket you purchased:-----------")
                    print("\nMovie: ", movie_chosen)
                    print("\nSlot: ", time_chosen)
                    print("\nSeat: ", seat_chosen)
                    print("\nPrice: $", PRICE)

                    #Check if a slot is full
                    cur.execute('SELECT * FROM Ticket WHERE slot_id = ?', (slot_id,))
                    ordered_tickets = cur.fetchall()
                    #Update slot isFull to 1 if the slot is full
                    if len(ordered_tickets) == CAPACITY:
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

                    #print purchased tickets
                    print("\n-----Ticket %d-----"%(i + 1))
                    print("\nMovie: ", movie_purchased)
                    print("\nSlot: ", time_purchased)
                    print("\nSeat: ", tickets_purchased[i][2])
                    print("\nPrice: $", PRICE)
        
            elif choice == 3:
                #log out
                is_logged_in = False
            
            conn.commit()
        

if __name__ == '__main__':

    conn = sqlite3.connect('cinema.sqlite')
    cur = conn.cursor()

    try:
        booking()
    except Exception as e:
        print('\nYour session has timed out, please try again!')


    # close database upon timeout
    conn.close()
