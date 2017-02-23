import sqlite3



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





seats=['A','B','C','D','E']

for i in range(1,21):
	for seat in seats:
		fillTable('data.db',i,seat)


print("Database updated")