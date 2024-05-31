import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database="mydb",
  autocommit=True
)

def getDBConnection() :
  return mydb.cursor()