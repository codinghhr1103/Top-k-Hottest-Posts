import sqlite3

#Connecting to sqlite
conn = sqlite3.connect('/home/laphy/Top_K_Hottest/TopK.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS DailyReport")
cursor.execute("DROP TABLE IF EXISTS FrequentReport")

#Creating table for daily report
sql ='''CREATE TABLE DailyReport(
   URL VARCHAR(255) PRIMARY KEY,
   cnt INT
)'''
cursor.execute(sql)

#Creating table for frequent report
sql ='''CREATE TABLE FrequentReport(
   URL VARCHAR(255) PRIMARY KEY,
   cnt INT
)'''
cursor.execute(sql)

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()


