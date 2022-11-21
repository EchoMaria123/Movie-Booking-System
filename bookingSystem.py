import sqlite3

conn = sqlite3.connect('cinema.sqlite')
cur = conn.cursor()

isLoggedIn = False

#Welcome
print("\n********************WELCOME TO LALALAND MOVIE BOOKING TICKET SYSTEM***********************")
#Sign up / in
print("\n Please enter your email address and password; if you don't have an account with us, we will automatically create one for you ^_^")

while (isLoggedIn == False):

    emailInput = input("\nPlease enter your email address: ")

    cur.execute('SELECT * FROM User WHERE email = ? ', (emailInput, ))
    userFound = cur.fetchone()

    #If there's no such user, we just create a new one
    if (userFound == None): 
        password = input("\nPlease set up your password: ")
        cur.execute('INSERT INTO User (email, password) values (?, ?)', (emailInput, password))
        isLoggedIn = True
        print("\n------------A new account has been created!------------")
    #If the user exists
    else:
        password = input("\nPlease enter your password:")
        passwordFound = userFound[2]
        #If the password is correct
        if (password == passwordFound):
            isLoggedIn = True
            print("\n-----------Logged in successfully!-----------")
        #Otherwise
        else:
            print("Wrong password! Please try again!")

#Buy tickets
    #Return all genres
    #Only 3 genres in our case
        #Return all movies
            #Return all available slots (isFull = 0)
                #Return all seats available
                #User select 
                    #If the entered seat is not available, print something (this could be omitted if we assume every input is valid)
                    #Otherwise, insert a new ticket and print detailed information
                        #If SELECT count (*) from Ticket WHERE slot_id = XXXX is 9, 
                        #UPDATE Slot SET isFull = 1 WHERE id = XXXXX

#View tickets bought



conn.commit()

cur.close()