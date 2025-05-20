import mysql.connector
from mysql.connector import Error

def init_database():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS chessdb")
            cursor.execute("USE chessdb")
            
            # Read and execute the SQL file
            with open('code/triggers.sql', 'r') as sql_file:
                sql_commands = sql_file.read()
                
                # Split the commands by delimiter
                commands = sql_commands.split('$$')
                
                for command in commands:
                    if command.strip():
                        try:
                            cursor.execute(command)
                            connection.commit()
                        except Error as e:
                            print(f"Error executing command: {e}")
                            print(f"Command was: {command[:100]}...")  # Print first 100 chars of the command
                            continue

            print("Database initialized successfully!")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    init_database() 