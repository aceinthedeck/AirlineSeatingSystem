import sqlite3
import csv
import random



# This program fills the database for testing 							#
# fillRowsColsTable function fills the seating arrangement				#
# fillTable fills the seating table according to the seating arrangment #


def clearSeatingTable(fileName):
	conn=sqlite3.connect(fileName)
	c=conn.cursor()
	cmd='Delete from seating'
	try:
		c.execute(cmd)
		conn.commit()
		conn.close()
	except sqlite3.Error as er:
		print(er.message)
		conn.close()

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
		for name in nameList:
			fileWriter.writerow([name[0],random.randint(1,5)])


def getNames(fileName):
	names=[]
	try:
		with open(fileName) as f:
			reader=csv.reader(f)
			for row in reader:
				names.append(row)
			return names
	except:
		print("Unable to open the file containing random names")

randomNames=[]
namesCSV='names.csv'
fileName='data.db'
seats='ABCDE'
totalRows=20
cols=0

randomNames=getNames(namesCSV)
createBookingsCSV('test.csv',randomNames)

print("Testfile created")

clearSeatingTable(fileName)

fillRowsColsTable(fileName,totalRows,seats)

for i in range(1,totalRows+1):
	for seat in seats:
		fillTable(fileName,i,seat)

print("Database updated")