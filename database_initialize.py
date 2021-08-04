import sqlite3

#Connecting to sqlite
conn = sqlite3.connect(r'C:\Users\hhrh1\Desktop\Top K Hottest\TopK.db')

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS DailyReport")

#Creating table as per requirement
sql ='''CREATE TABLE DailyReport(
   URL VARCHAR(255) PRIMARY KEY,
   cnt INT
)'''
cursor.execute(sql)
print("Table created successfully........")

# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()