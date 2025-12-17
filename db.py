import mysql.connector
from mysql.connector import Error
from config import Config

def get_db():
    """
    Membuat dan mengembalikan koneksi MySQL.
    Dipakai oleh semua controller yang butuh akses database.
    """

    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASS,
            database=Config.DB_NAME
        )
        return connection

    except Error as e:
        print("Error connecting to MySQL:", e)
    return None