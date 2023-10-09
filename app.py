from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = "entersecretkeyofchoicehere"

# Set up the db
def create_table():
    conn = sqlite3.connect('form_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS form_entries
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       surname TEXT NOT NULL,
                       othernames TEXT NOT NULL,
                       location TEXT NOT NULL,
                       department TEXT NOT NULL,
                       tel TEXT NOT NULL,
                       email TEXT NOT NULL,
                       calender TEXT NOT NULL,
                       one TEXT NOT NULL,
                       two TEXT NOT NULL,
                       three TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def create_users_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL,
                       password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

#create_table()
#create_users_table()

def insert_admin_user():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    admin_username = 'enterusernamehere'
    admin_password_hash = 'enterhashedpassword'

    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (admin_username, admin_password_hash))
    conn.commit()
    conn.close()

#insert_admin_user()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        surname = request.form['surname']
        othernames = request.form['othernames']
        location = request.form['location']
        department = request.form['department']
        tel = request.form['tel']
        email = request.form['email']
        calender = request.form['calender']
        one = request.form['one']
        two = request.form['two']
        three = request.form['three']

        # Connect to the db
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()

        # Insert form data
        cursor.execute('INSERT INTO form_entries (surname, othernames, location, department, tel, email, calender, one, two, three) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (surname, othernames, location, department, tel, email, calender, one, two, three))

        conn.commit()
        conn.close()

        return redirect('/success')  

    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(type(password))
        print(username)
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
         session['username'] = user[1]  # Store username in session
         return redirect(url_for('data_table'))
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('admin.html', error_message=error_message)

    return render_template('admin.html')

@app.route('/data_table', methods=['GET'])  # handles only GET requests
def data_table():
    if 'username' in session:
        conn = sqlite3.connect('form_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM form_entries')
        form_data = cursor.fetchall()
        conn.close()

        return render_template('data_table.html', form_data=form_data)
    else:
        return redirect(url_for('admin'))  # Redirect to admin route if not authenticated

if __name__ == '__main__':
    app.debug = True
    app.run()
