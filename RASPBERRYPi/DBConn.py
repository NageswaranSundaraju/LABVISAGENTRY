# DBCONNECTION.py
import mysql.connector

dbstat = ""  # Initialize dbstat

def condb():
    global dbstat
    try:
        cnx = mysql.connector.connect(
            user='NAGES',
            password='ROOT',
            host='192.168.0.254',
            database='mydatabase'
        )
        if cnx.is_connected():
            print('db is connect')
            dbstat = "DB is Connected"
            return cnx
        else:
            print('db is not connected')
            dbstat = "DB Failed to Connect"
            return None
    except mysql.connector.Error as err:
        print(err.errno)
        if err.errno == 1045:
            dbstat = "DB ACCESS DENIED"
        else:
            dbstat = 'DB IS FAILED CONNECTED'

        return None

condb()