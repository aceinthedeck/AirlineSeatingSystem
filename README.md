# MIS40750AirlineSeating
Analytics Research And Implementation

###1.Database Structure

The program assumes the following database structure:
    
    1. Metrics table
        passengers_refused integer
        passengers_separated integer
    
    2. rows_cols table
        nrows  integer
        seats  string
    
    3. seating table
        row integer
        seat char
        name string

###2. Program Structure

    The program is divided into three classes
    1. seatAllocator
    2. database
    3. readCSV
         
__seatAllocator__: This class contains information about seating arrangement and available seats. This class manages the booking of the passengers. It   an object of database as a member which enables it to call functions to connect and update the database

__database__: This class contains functions to connect and retreive information from the database

__readCSV__: This class connects and read information from the CSV file


###3. Running The Program

The program can be run by giving the following command
main.py data.db bookings.csv
where main.py is the name of the program, data.db is the name of the SQLite database and bookings.csv contains the bookings data

###4. CSV file structure

The program assumes that there are two columns in the CSV file. First coloumn contains the name of the passenger and the second column indicates the number of seats requested by the passenger in the first column

###5.Sample Testing

There is a seperate program for testing which is __filltable.py__

    1. The file reads the csv file names.csv.
    2. The file updates the database data.db
    3. It generates a test.csv file with random names and bookings.
    4. It also clears and fills the seating table and row_cols table.

__Usage__:
... The file has following variables
... Line 82: testCSV
... Line 83: fileName
... Line 84: seats
... Line 85: totalRows
... Line 91: maxSeats

* testCSV is the desired name of the output csv. By default it is set to 'test.csv'
* fileName is the name of the database. By default it is set to 'data.db'
* seats variable determines the seats in a row eg 'ABCD' is a valid value
* totalRows variable sets the database to the number of rows available.
* maxSeats is a variable which determines the random number which will be generated to fill the csv file. This is the maximum value which the random number can take. By default it is set to number of seats in a row. eg for seats='ABCD' the maxSeats would be set to 4 by default.


