import sqlite3
import pickle
import os
import numpy as np
from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'MpHoMabidikama@1999'


# Create SQLite capstone and table
conn = sqlite3.connect('capstonedb.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)''')
conn.commit()
conn.close()


# Function to hash the password
def hash_password(password):
    return generate_password_hash(password)

# Function to verify hashed password
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        # role = request.form['role']
        password = request.form['password']

        # Hash the password
        hashed_password = hash_password(password)

        conn = sqlite3.connect('capstonedb.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username,  password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        return render_template('login.html')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('capstonedb.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and verify_password(user[2], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials. Please try again.'

    return render_template('login.html')



@app.route('/')
def home():
    username = session.get('username')
    if username:
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


# model predictions

# Import the model as pickle file
with open('Construction.pkl','rb') as capstone_model:
        model = pickle.load(capstone_model)


# Run predictions 
@app.route('/predict', methods=['POST'])
def ml_route():
    if request.method == 'POST':
        data = request.get_json()
  
        laborers = data['laborers']
        cash_flow = data['cash_flow']
        Errors = data['Errors']
        communication = data['communication']
        Change_schedule = data['Change_schedule']
        bid_price = data['bid_price']
        scope_change = data['scope_change']
        Weather_conditions = data['Weather_conditions']
        Accidents = data['Accidents']


        # Reshape features and make prediction using the loaded model
        features = np.array([[laborers, cash_flow, Errors, communication,Change_schedule, bid_price, scope_change, Weather_conditions, Accidents]])
        prediction = model.predict(features)[0]

        return jsonify({'prediction': prediction.tolist()})
    

# add data to the data base
import sqlite3

@app.route('/upload', methods=['POST'])
def update_DB():
    if request.method == 'POST':
        data = request.get_json()

        # Extract data from the JSON
        Delay = data['Delay']
        laborers = data['laborers']
        cash_flow = data['cash_flow']
        Errors = data['Errors']
        communication = data['communication']
        Change_schedule = data['Change_schedule']
        bid_price = data['bid_price']
        scope_change = data['scope_change']
        Weather_conditions = data['Weather_conditions']
        Accidents = data['Accidents']

        # Connect to the SQLite database
        conn = sqlite3.connect('capstonedb.db')
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute("INSERT INTO delays (Delay, laborers, cash_flow, Errors, communication, Change_schedule, bid_price, scope_change, Weather_conditions, Accidents) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (Delay, laborers, cash_flow, Errors, communication, Change_schedule, bid_price, scope_change, Weather_conditions, Accidents))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return 'Data successfully added to the database'





# read database and store historical values
@app.route('/api/historical_data/', methods=['GET'])
def get_historical():
    conn = sqlite3.connect('capstonedb.db')
    cursor = conn.cursor()

    cursor.execute('SELECT Delay, laborers, cash_flow, Errors, communication, Change_schedule, bid_price, scope_change, Weather_conditions, Accidents FROM delays ORDER BY id DESC LIMIT 3')
    rows = cursor.fetchall()

    conn.close()

    # Define the column names
    column_names = ['Delay', 'laborers', 'cash_flow', 'Errors', 'communication', 'Change_schedule', 'bid_price', 'scope_change', 'Weather_conditions', 'Accidents']

    # Convert the fetched rows to a list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]

    # Return the data as JSON
    return jsonify({'historical_data': data})



# read database and store historical values
@app.route('/api/ALL_historical_data/', methods=['GET'])
def get_ALL_historical():
    conn = sqlite3.connect('capstonedb.db')
    cursor = conn.cursor()

    cursor.execute('SELECT Delay, laborers, cash_flow, Errors, communication, Change_schedule, bid_price, scope_change, Weather_conditions, Accidents FROM delays ORDER BY id DESC LIMIT 30')
    rows = cursor.fetchall()

    conn.close()

    # Define the column names
    column_names = ['Delay', 'laborers', 'cash_flow', 'Errors', 'communication', 'Change_schedule', 'bid_price', 'scope_change', 'Weather_conditions', 'Accidents']

    # Convert the fetched rows to a list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]

    # Return the data as JSON
    return jsonify({'historical_data': data})




# get tasks assigned
@app.route('/api/tasks/', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('capstonedb.db')
    cursor = conn.cursor()

    cursor.execute('SELECT Name, Duration, AssignedTo, status FROM tasks ORDER BY id DESC LIMIT 7')
    rows = cursor.fetchall()

    conn.close()

    # Define the column names
    column_names = ['Name', 'Duration', 'AssignedTo', 'status']

    # Convert the fetched rows to a list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]

    # Return the data as JSON
    return jsonify({'tasks': data})


# get tasks assigned
@app.route('/api/ALL_tasks/', methods=['GET'])
def get_ALL_tasks():
    conn = sqlite3.connect('capstonedb.db')
    cursor = conn.cursor()

    cursor.execute('SELECT Name, Duration, AssignedTo, status FROM tasks ORDER BY id DESC LIMIT 35')
    rows = cursor.fetchall()

    conn.close()

    # Define the column names
    column_names = ['Name', 'Duration', 'AssignedTo', 'status']

    # Convert the fetched rows to a list of dictionaries
    data = [dict(zip(column_names, row)) for row in rows]

    # Return the data as JSON
    return jsonify({'tasks': data})


@app.route('/addtask', methods=['POST'])
def add_task():
    if request.method == 'POST':
        data = request.get_json()

        # Extract data from the JSON
        Name = data['Name']
        Duration = data['Duration']
        AssignedTo = data['AssignedTo']
        status = data['status']
        

        # Connect to the SQLite database
        conn = sqlite3.connect('capstonedb.db')
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute("INSERT INTO tasks (Name, Duration, AssignedTo, status) VALUES (?, ?, ?, ?)",
                       (Name, Duration, AssignedTo, status))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return 'Data successfully added to the database'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predictions')
def predictions():
    return render_template('predictions.html')

@app.route('/Task')
def task():
    return render_template('task.html')

@app.route('/report')
def report():
    return render_template('report.html')



if __name__ == '__main__':
    app.run(debug=True)


