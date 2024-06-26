# DBCONNECTION.py
import mysql.connector

dbstat = ""  # Initialize dbstat

def condb():
    global dbstat
    try:
        cnx = mysql.connector.connect(
            user='Nages',
            password='admin',
            host='192.168.187.142',
            database='lve_user'
        )
        if cnx.is_connected():
            print('db is connected')
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