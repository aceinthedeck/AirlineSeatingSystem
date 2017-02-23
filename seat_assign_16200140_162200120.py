import sqlite3
import csv
import sys
import os.path



class readCSV(object):

	def __init__(self,fileName):
		self.fileName=fileName
		self.bookingData=[]

	#reads csv file into bookingData variable
	def readFile(self):
		try:
			with open(self.fileName) as f:
				reader=csv.reader(f)
				for row in reader:
					self.bookingData.append(row)
		except:
			print("Unable to open the file containing booking data.")


class database(object):

	def __init__(self,fileName):
		self.fileName=fileName
		self.seatChars=[]

	#returns number of the rows in the plane from the database
	def getRows(self):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		try:
			c.execute('Select nrows from rows_cols')
			rows = c.fetchone()[0]
			conn.close()
			return rows
		except sqlite3.Error as er:
			print(er.message)
			conn.close()
			return -1

			

	#returns number of columns in the plane and get column codes for seats from the database
	def getColumns(self):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		try:
			c.execute('Select seats from rows_cols')
			cols = c.fetchone()[0]
			count=0
			for char in cols:
				self.seatChars.append(char)
				count=count+1
			conn.close()
			return count
		except sqlite3.Error as er:
			print(er.message)
			return -1

	#get maximum available seats by each row
	def getMaxAvailableSeats(self):

		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		remainingSeats=self.getRemainingSeats()
		if(remainingSeats>0):
			try:
				c.execute('select count(seat)from seating where name="" group by row order by count(seat) desc')
				maxSeatsInARow=c.fetchone()[0]
				conn.close()
			except sqlite3.Error as er:
				print(er.message)
				conn.close()
				maxSeatsInARow=0
		else:
			maxSeatsInARow=0
		print("Maximum available seats {}".format(maxSeatsInARow))
		return maxSeatsInARow

	#returns the absolute number of remaining seats
	def getRemainingSeats(self):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select count(seat) from seating where name=""'
		c.execute(cmd)
		totalEmptySeats=c.fetchone()[0]
		conn.close()
		return totalEmptySeats

	#returns the number of empty seats in a row
	def getEmptySeatsInRow(self, rowNumber):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select count(seat) from seating where row=(?) and name=""'
		try:
			c.execute(cmd,(rowNumber,))
			emptySeats=c.fetchone()[0]
			conn.close()
		except:
			print("Error in connecting to database")
		return emptySeats

	#resets the metrics table in the database
	def cleanUp(self):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='update metrics set passengers_refused=0, passengers_separated=0'
		try:
			c.execute(cmd)
			conn.commit()
		except sqlite3.Error as er:
			print(er.message)
			conn.close()

	#return the list of rows having empty seats more than required sets
	def getEmptyRowBySeats(self,requiredSeats):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select row,count(seat) as numOfSeats from seating  where name="" group by row  having numOfSeats>=(?)'
		try:
			c.execute(cmd,(requiredSeats,))
			rowNumber=c.fetchone()[0]
			conn.close()
			return rowNumber
		except sqlite3.Error as er:
			print(er.message)
			conn.close()
			return -1

	#return the array of seats available by row
	def getEmptySeatsArray(self,row):
		seats=[]
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select seat from seating where row=(?) and name=""'
		try:
			c.execute(cmd,(row,))
			for row in c:
				seat=row[0]
				seats.append(seat)
			conn.close()
			return seats
		except:
			print("Unable to connect with database")


	#saves the details of the booked seats in the database
	def addBookedSeatsRecord(self,row,seat,name):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Update seating set name=(?) where row=(?) and seat=(?)'
		try:
			c.execute(cmd,(name,row,seat))
			conn.commit()
			rowsCount=c.rowcount
			if rowsCount>0:
				conn.close()
				return rowsCount
			else:
				print("error in adding the seat to database")
				conn.close()
				return -1
		except sqlite3.Error as er:
			print(er.message)
			conn.close()

	#get the number of refused bookings from the database
	def getRefusedBookings(self):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Select passengers_refused from metrics'
		try:
			c.execute(cmd)
			refusedBookings=c.fetchone()[0]
			conn.close()
		except sqlite3.Error as er:
			print(er.message)
			conn.close()

	#update the number of refused bookings in the database
	def updateRefusedBookings(self,refusedBookings):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Update metrics set passengers_refused=passengers_refused+(?)'
		try:
			c.execute(cmd,(refusedBookings,))
			conn.commit()
			rowsCount=c.rowcount
			if rowsCount>0:
				conn.close()
				return rowsCount
			else:
				print("error in updating refused bookings")
				conn.close()
				return -1
		except sqlite3.Error as er:
			print(er.message)
			conn.close()

	#update the number of seperated passengers
	def updateSeperatedBookings(self,seperatedBookings):
		conn=sqlite3.connect(self.fileName)
		c=conn.cursor()
		cmd='Update metrics set passengers_separated=passengers_separated+(?)'
		try:
			c.execute(cmd,(seperatedBookings,))
			conn.commit()
			rowsCount=c.rowcount
			if rowsCount>0:
				conn.close()
				return rowsCount
			else:
				print("error in updating refused bookings")
				conn.close()
				return -1
		except sqlite3.Error as er:
			print(er.message)
			conn.close()


class seatAllocator(database):

	def __init__(self,rows,columns,dbName):
		self.maxSeats=rows*columns
		self.rows=rows
		self.columns=columns
		self.seatsAvailable=self.maxSeats
		self.maxSeatsInARow=columns
		self.seatsBooked=0
		self.bookingsRefused=0
		self.awayPassengers=0
		self.seatsInRow=self.maxSeats/columns
		self.seatChars=[]
		database.__init__(dbName)


	def printInfo(self):
		print("Maximum number of seats: {}".format(self.maxSeats))
		print("Number of rows: {}".format(self.rows))
		print("Number of columns: {}".format(self.columns))
		print("Number of seats in a row: {}".format(self.seatsInRow))

	#checks if seats are available
	def checkSeats(self,requestedSeats):
		if(self.seatsAvailable<requestedSeats):
			print("Seats not available")
			self.bookingsRefused+=requestedSeats
			print("Total bookings refused till now {}".format(self.bookingsRefused))


	#books seats in a single row
	def bookSeatsInARow(self,row,numberOfSeats,name):
		seats=database.getEmptySeatsArray(row)
		if seats:
			count=0
			for seat in seats:
				if count<numberOfSeats:
					bookingResult=database.addBookedSeatsRecord(row,seat,name)
					if bookingResult==1:
						count+=1
					else:
						print("Error in booking of seats")
			#update the maximum available seats in a row
			self.maxSeatsInARow=database.getMaxAvailableSeats()
			print("{} seat(s) booked successfully for {}".format(numberOfSeats,name))

	#book the seats
	def bookSeats(self,numberOfSeats,name):
		
		print("Attempting to book {} seats for {}".format(numberOfSeats,name))
		#get total seats remaining
		remainingSeats=database.getRemainingSeats()
		seats=[]
		#check with remaining seats
		if(numberOfSeats<=remainingSeats):
			
			#check if passengers can be accomodated in a single row
			if(numberOfSeats<=self.maxSeatsInARow):
				bookedRow=database.getEmptyRowBySeats(numberOfSeats)
				if(bookedRow==-1):
					print("No seats available")
				else:
					self.bookSeatsInARow(bookedRow,numberOfSeats,name)

			# else divide the seats and book in seperate rows
			else:
				numberOfRows=numberOfSeats//self.maxSeatsInARow
				extraSeats=numberOfSeats%self.maxSeatsInARow
				print("Booking {} + {} seats".format(numberOfRows,extraSeats))
				database.updateSeperatedBookings(numberOfSeats)
				for i in range(0,numberOfRows):
					bookedRow=database.getEmptyRowBySeats(self.maxSeatsInARow)
					if(bookedRow==-1):
						print("No seats available")
					else:
						self.bookSeatsInARow(bookedRow,self.maxSeatsInARow,name)

				if extraSeats>0:
					bookedRow=database.getEmptyRowBySeats(extraSeats)
					self.bookSeatsInARow(bookedRow,extraSeats,name)

		else:
			print("Not enough seats available. Remaining seats are {}".format(remainingSeats))
			self.bookingsRefused+=numberOfSeats
			database.updateRefusedBookings(numberOfSeats)
			print("booking refused till now {}".format(self.bookingsRefused))

if len(sys.argv)!=2:
	dbName=sys.argv[1]
	bookingsFile=sys.argv[2]
else:
	print("Insufficient number of command line arguments.")
	print("The correct format is <database name> <bookings csv file name>")
	exit()

if  not os.path.exists(dbName):
	print("Database file doesn't exists")
	exit()

if  not os.path.exists(bookingsFile):
	print("CSV file doesn't exists")
	exit()

database=database(dbName)
rows=database.getRows()
cols=database.getColumns()

#reset metrics taable
database.cleanUp()

booking=seatAllocator(rows,cols,dbName)
booking.seatChars=database.seatChars
booking.printInfo()


totalEmptySeats=database.getRemainingSeats()
print('remaining seats: {}'.format(totalEmptySeats))

readCSV=readCSV(bookingsFile)
readCSV.readFile()

for row in readCSV.bookingData:
	booking.bookSeats(int(row[1]),row[0])
	
