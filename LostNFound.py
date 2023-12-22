from flask import Flask, render_template, request, redirect, url_for
from datetime import date
import subprocess
import psycopg2
import sys
import ast
import base64

app = Flask(__name__)

def Conn2db():
    conn = psycopg2.connect(
        user="postgres",
        password="1234",
        host="localhost",
        port="5432",
        database="winterproject"
    )
    return conn

# Handle login
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = Conn2db()
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM users WHERE uname = %s AND upass = %s', (username, password))
            result = cursor.fetchall()

            if len(result) > 0:
                if (result[0][-1] == True):
                    return redirect('/main_admin')
                else:
                    return redirect('/main_user')
            else:
                return 'Invalid username or password'
        except psycopg2.Error as e:
            return 'Error: {}'.format(str(e))
        finally:
            cursor.close()
            conn.close()
    return render_template('login.html')

# Handle signup
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = Conn2db()
        cursor = conn.cursor()

        try:
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS users (
                    uid SERIAL PRIMARY KEY,
                    uname VARCHAR(100) UNIQUE,
                    upass INT,
                    admin BOOL
                );
            '''
            insert_query = '''
                INSERT INTO users (uname, upass, admin) VALUES (%s, %s, %s);
            '''
            cursor.execute(create_table_query)
            cursor.execute(insert_query, (username, password, False))
            conn.commit()
            return redirect('/')
        except psycopg2.Error as e:
            return 'Signup failed: {}'.format(str(e))
        finally:
            cursor.close()
            conn.close()
    return render_template('signup.html')

@app.route('/main_user', methods=['GET'])
def main_user():
    return render_template('main_user.html')

@app.route('/main_admin', methods=['GET'])
def main_admin():
    return render_template('main_admin.html')

@app.route('/lost', methods=['GET','POST'])
def lost():
    if request.method == 'POST':
        description = request.form['description']
        python_exe = sys.executable
        cmd = [str(python_exe), "JaccardRanker.py"]
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        results, errors = process.communicate(input=description)
        results = ast.literal_eval(results)
        print(results)
        return render_template('lost.html', results=results)  # Assuming results are separated by lines
    return render_template('lost.html', results=None)

@app.route('/details/<int:item_id>')
def item_details(item_id):
    conn = Conn2db()
    cursor = conn.cursor()
    cursor.execute('SELECT iid, ides, iimage FROM items WHERE iid = %s', (item_id,))
    item_details = cursor.fetchone()
    cursor.close()
    conn.close()
    print(item_details)
    if item_details[2]:
        encoded_image = base64.b64encode(item_details[2]).decode('utf-8')
    return render_template('details.html', item_details=item_details[:2]+(encoded_image,))

@app.route('/claim/<int:item_id>', methods=['POST'])
def claim_item(item_id):
    conn = Conn2db()
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET claims = claims + 1 WHERE iid = %s;', (item_id,))
    conn.commit()
    conn.close()
    return "Claim placed succesfully!"

# Display the /found page
@app.route('/found')
def found():
    return render_template('found.html')

# Handle submission of found item details
@app.route('/submit_found', methods=['POST'])
def submit_found():
    try:
        conn = Conn2db()
        cursor = conn.cursor()

        description = request.form['description']
        username = request.form['username']
        image = request.files['image'] if 'image' in request.files else None

        if image:
            # If an image is uploaded, store it in the database
            image_data = image.read()
            cursor.execute("INSERT INTO items (ides, iimage, claims, found, cdate, collected) VALUES (%s, %s, %s, %s, %s, %s);",
                           (description, psycopg2.Binary(image_data), 0, username, None, None))
        else:
            # If no image is uploaded, set iimage column as NULL
            cursor.execute("INSERT INTO items (ides, iimage, claims, found, cdate, collected) VALUES (%s, %s, %s, %s, %s, %s);",
                           (description, None, 0, username, None, None))

        conn.commit()
        conn.close()
        return "Item found successfully reported!"
    except Exception as e:
        conn.rollback()
        return f"Failed to report found item. Error: {str(e)}", 500

# Display the /modify page
@app.route('/modify')
def modify():
    return render_template('modify.html')

# Handle modification of an item
@app.route('/modify_item', methods=['POST'])
def modify_item():
    try:
        conn = Conn2db()
        cursor = conn.cursor()

        item_id = request.form['item_id']
        collected_by = request.form['collected_by']

        # Update cdate and collected columns for the specified item_id
        today_date = date.today()
        cursor.execute("UPDATE items SET cdate = %s, collected = %s WHERE iid = %s;",
                       (today_date, collected_by, item_id))
        
        conn.commit()
        conn.close()
        return "Item updated successfully!"
    except Exception as e:
        conn.rollback()
        return f"Failed to update item. Error: {str(e)}", 500
    
if __name__ == '__main__':
    app.run(debug=True)
