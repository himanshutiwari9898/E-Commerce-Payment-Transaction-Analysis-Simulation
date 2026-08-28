import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass123",
        database="ecommerce"
    )

    return connection