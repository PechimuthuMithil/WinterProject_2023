import nltk
import psycopg2
import sys
import subprocess

def create_users(conn):
    # SQL query to create a table if it doesn't exist
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            uid SERIAL PRIMARY KEY,
            uname VARCHAR(100) UNIQUE,
            upass INT,
            admin BOOL
        );
    '''
    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()

def create_items(conn):
    # SQL query to create a table if it doesn't exist
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS items (
            iid SERIAL PRIMARY KEY,
            ides VARCHAR(1000),
            iimage BYTEA,
            claims INT,
            found VARCHAR(100),
            collected VARCHAR(100),
            cdate DATE
        );
    '''
    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

print("<<<<<<< Setting up Database >>>>>>>\n")
# Change these details accordingly.
conn = psycopg2.connect(
    dbname='winterproject',
    user='postgres',
    password='1234',
    host='localhost',
    port=5432
)
print("DONE!")
print("<<<<<<< Starting the Server >>>>>\n")
try:
    python_exe = sys.executable
    cmd = [str(python_exe), "LostNFound.py"]

    # Run the command using subprocess.run()
    subprocess.run(cmd)
except KeyboardInterrupt:
    print("Ctrl + C pressed. Shutting down server ...")
    # Perform cleanup or additional actions if needed
    sys.exit(0)  # Terminate the script or take necessary actions