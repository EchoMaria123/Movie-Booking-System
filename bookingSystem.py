import sqlite3

conn = sqlite3.connect('cinema.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM User')
print()

#Welcome
print("\n********************WELCOME TO LALALAND MOVIE BOOKING TICKET SYSTEM***********************")
#Sign up / in
print("\n Please enter your email address and password; if you don't have an account with us, we will automatically create one for you ^_^")

emailInput = input("\nPlease enter your email address:")
print(emailInput)
print(type(emailInput))
password = input("\nPlease enter your password:")
# check for email addr in User
#cur.execute('''SELECT * FROM User WHERE email=(?);''',(emailInput,))
cur.execute('SELECT id FROM User WHERE email = ? ', (emailInput,))

if(len(list(cur)) == 0): 
    print("you are right")

print(cur)
user_password = cur.fetchone()
print(user_password)


# pas = input("\nENTER YOUR PASSWORD:-")
# otp = int(input("\nENTER A OTP CODE ON YOUR EMAIL AND PHONE NO:-"))

# print("\n-------LOGIN SUCCESSFUL-------")



# print("\n-------YOUR accountOUNT IS CREATED SUCCESSFULLY-------")



conn.commit()

cur.close()