import sqlite3
import csv




# This program fills the database for testing 							#
# fillRowsColsTable function fills the seating arrangement				#
# fillTable fills the seating table according to the seating arrangment #

def fillTable(fileName,row,seat):
	conn=sqlite3.connect(fileName)
	c=conn.cursor()
	cmd='Insert into seating values(?,?,"")'
	try:
		c.execute(cmd,(row,seat))
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

def fillRowsColsTable(fileName,row,seats):
	conn=sqlite3.connect(fileName)
	c=conn.cursor()
	cmd='Update rows_cols set nrows=(?) and seats=(?)'
	try:
		c.execute(cmd,(row,seats))
		conn.commit()
		rowsCount=c.rowcount
		if rowsCount>0:
			conn.close()
			return rowsCount
		else:
			print("error in adding the seats to database")
			conn.close()
			return -1
	except sqlite3.Error as er:
		print(er.message)
		conn.close()

def createBookingsCSV(fileName,nameList):

	with open(fileName,'w',newline='') as csvFile:
		fileWriter=csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		fileWriter.writerow(['Ace',1])


createBookingsCSV('test.csv',['Ace'])
print("file created")

fileName='data.db'
seats='ABCDE'
totalRows=20

#fillRowsColsTable(fileName,totalRows,seats)

#for i in range(1,totalRows+1):
#	for seat in seats:
#		fillTable(fileName,i,seat)


#print("Database updated")