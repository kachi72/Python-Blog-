import mysql.connector

def connection():
    db = mysql.connector.connect(host = "localhost",user = "kachi",password = "kachiuser",db = "Blog")
    return db
