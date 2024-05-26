import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

database = mysql.connector.connect(
    host = 'localhost',
    user = os.getenv("USER"),
    passwd = os.getenv("PASSWORD"),
    auth_plugin='mysql_native_password'
)

cursorObject = database.cursor()

cursorObject.execute("CREATE DATABASE maindb")

print("All Done!")