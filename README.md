# Movie-Booking-System

## Introduction

Nowadays, watching movies has become one of the adults' most popular stress-release ways. Although movies can be watched on your laptop or electronic devices, going out to a cinema features many advantages that make it a fantastic movie-watching experience. However, frequent queues are common to see when customers try to buy movie tickets in the cinema branches. Some potential customers often complain about their seat choices when they are being late to purchase tickets in the cinema, which may cause a loss of customers.

Therefore, it is important for a cinema to have an automatic online ticket booking system to provide customers with faster and more accessible services. Thus, our team aims to develop a data-driven python application to provide a more convenient way for movie lovers to quickly browse the movie through current movie listings, choose the desired movie seats, and buy or reserve movie tickets anywhere, anytime.

## Database design

A movie has multiple slots and a slot has multiple tickets (3 and 9 in this case respectively). A user can purchase many tickets. We also created 3 genres, namely Romance, Comedy and Horror. There are 3 movies in each category. When all of the 9 seats have been booked for a slot, it will be marked as full and users can no longer buy tickets from this slot.

It is worth noting that all information in Movie and Slot is created by us beforehand. When a user is registered we will store it in the database. Likewise, only when a ticket is purchased will it be added to the Ticket table.

## Functionality

The booking system will allow users to sign up, sign in, log out, and purchase tickets. If the user does not have an account, we will automatically create one and insert the entry to the database. Otherwise, the user will have to enter the password until it is correct. When the user has successfully purchased a ticket, there will be a summary of the user’s ticket order on the screen.

After the user has signed in, there are 3 options that the user can choose from:

- Buy tickets. We’ll be storing data in SQLite. When purchasing the tickets, the system will first return a list of all available genres and the user will choose a genre, then the name of the movie, choose their preferred time slot, seat. When the genre, movie name, time slot and seat have been selected and confirmed, an email will be sent out by our system automatically.
- View tickets. Our system will print out the information of all tickets the user has bought.
- Log out. That way the user will have to sign up / sign in again to access our system.

## To run the code

- git clone this project
- cd to the project directory
- run
  ```python
  python cinema_CRUD.py
  ```
  to initialize an empty database
- run
  ```python
  python bookingSystem.py
  ```
  to run the project
- also do not forget to download all the packages if needed :)
