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

3.Sample Testing

