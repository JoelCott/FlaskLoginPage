from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to the database
cnx = mysql.connector.connect(user='your_username',
                              password='your_password',
                              host='your_host',
                              database='your_database')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    # Get the user's input from the form
    username = request.form['username']
    password = request.form['password']

    # Create a cursor
    cursor = cnx.cursor()

    # Check if the user exists in the database
    query = 'SELECT * FROM users WHERE username = %s AND password = %s'
    cursor.execute(query, (username, password))

    # Fetch the results
    results = cursor.fetchall()

    # If the user exists, log them in
    if results:
        session['username'] = username
        return redirect('/dashboard')

    # If the user doesn't exist, redirect to the login page
    else:
        return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    # Get the user's input from the form
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    cursor = cnx.cursor()
    query = 'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)'
    cursor.execute(query, (username, password, email))
    cnx.commit()
    cursor.close()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
