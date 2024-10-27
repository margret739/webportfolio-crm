# install Mysql on computer
# pip install mysql
# pip install mysql-connector

import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'maggie',
    passwd = 'password3948',

    )

# preparing a cursor object
cursorObject = dataBase.cursor()

# create a database
cursorObject.execute("CREATE DATABASE cdata")

print("All Done!")
