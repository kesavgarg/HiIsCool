from flask import Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
from mysql.connector import Error
from config import db_config  # Ensure this is correctly configured
from werkzeug.security import generate_password_hash
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for sessions

# Home route
@app.route('/')
def home():
    return render_template('index.html')
    # if 'user' in session:
    #     return render_template('index.html', user=session['user'])
    # return redirect('/login')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                session['user'] = username
                flash(f'Welcome back, {username}!')
                return redirect('/')
            else:
                flash('Invalid username or password.')
        except Error as e:
            flash(f'Database error: {e}')
    return render_template('login.html')

# Jobs page
@app.route('/addNewJob')
def jobs():
    return render_template('postJobs.html')

# @app.route('/passcode')
# def passcode():
#     return render_template('passcode.html')

# Hiring page
@app.route('/jobs')
def hiring():
    return render_template('jobs.html')

# FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')

# TOS page
@app.route('/terms')
def terms():
    return render_template('terms.html')

# Privacy page
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/contactUs')
def contact():
    return render_template('contactUs.html')

# Add jobs route
@app.route('/addjobs1', methods=['POST'])
def addJobs1():
    if 'user' not in session:
        return redirect('/login')

    try:
        # Parse job details from the request body
        # data = request.get_json()
        # jobTitle = data.get('jobTitle')
        # jobDescription = data.get('jobDescription')
        # companyName = data.get('companyName')
        # jobLocation = data.get('jobLocation')
        # baseSalary = data.get('baseSalary')
        jobTitle = request.form['jobTitle']
        jobDescription = request.form['jobDescription']
        companyName = request.form['companyName']
        jobLocation = request.form['jobLocation']
        baseSalary = request.form['baseSalary']
        flash('XXXX ' + jobTitle)

        # Validate input
        # if not jobTitle or not jobDescription or not companyName or not jobLocation:
        #     return jsonify({'error': 'All fields are required'}), 400

        # Connect to the database and insert job
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO jobs (job_title, job_description, company_name, salary, job_location)
            VALUES (%s, %s, %s, %s, %s)
        ''', (jobTitle, jobDescription, companyName, baseSalary, jobLocation))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Job added successfully!'}), 201
    except Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {e}'}), 500

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Received data: {data}")
        email = data.get('email')
        password = data.get('password')
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (email, hashed_password))
            conn.commit()
            conn.close()

            flash('Registration successful! Please log in.')
            return redirect('/login')
        except mysql.connector.IntegrityError:
            #flash('Username already exists.')
            print('Username already exists.')
        except Error as e:
            #flash(f'Database error: {e}')
            print(f'Database error: {e}')
    return render_template('register.html')

# Register route
@app.route('/register1', methods=['GET', 'POST'])
def register1():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Received data: {data}")
        username = data.get('student-username')
        school = data.get('school')
        print(f"Received data:" + username + school)
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            conn.close()

            flash('Registration successful! Please log in.')
            return redirect('/login')
        except mysql.connector.IntegrityError:
            flash('Username already exists.')
        except Error as e:
            flash(f'Database error: {e}')
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.')
    return redirect('/login')

# Add jobs route
@app.route('/addJobs', methods=['POST'])
def addJobs():
    try:
        # Parse job details from the request body
        data = request.get_json()
        print(f"Received data: {data}")
        jobTitle = data.get('jobTitle')
        jobDescription = data.get('jobDescription')
        companyName = data.get('companyName')
        jobLocation = data.get('jobLocation')
        baseSalary = data.get('baseSalary')

        # Validate input
        if not jobTitle or not jobDescription or not jobLocation or not companyName:
            return jsonify({'error': 'All fields are required'}), 400

        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert the job into the database
        cursor.execute('''
            INSERT INTO jobs (job_title, job_description, company_name, salary, job_location)
            VALUES (%s, %s, %s, %s, %s)
        ''', (jobTitle, jobDescription, companyName, baseSalary, jobLocation))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Job added successfully!'}), 201
    except Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {e}'}), 500

@app.route('/getJobs', methods=['GET'])
def get_jobs():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT job_title AS jobTitle, job_description AS jobDescription, company_name AS companyName, salary AS baseSalary, job_location AS jobLocation FROM jobs")
        jobs = cursor.fetchall()
        conn.close()
        return jsonify(jobs)
    except Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
