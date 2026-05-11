from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = "quitwise"

# LOGIN PAGE

@app.route('/')
def login():
    return render_template('login.html')

# SIGNUP PAGE

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('health.db')
        cursor = conn.cursor()

        cursor.execute(
        '''
        INSERT INTO users(
        username,
        email,
        password
        )
        VALUES(?,?,?)
        ''',
        (
        username,
        email,
        password
        )
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('signup.html')

# LOGIN AUTHENTICATION

@app.route('/login', methods=['POST'])
def login_user():

    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('health.db')
    cursor = conn.cursor()

    cursor.execute(
    '''
    SELECT * FROM users
    WHERE email=? AND password=?
    ''',
    (
    email,
    password
    )
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        session['user_id'] = user[0]

        return redirect('/dashboard')

    else:

        return "Invalid Email or Password"

# DASHBOARD

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/')

    conn = sqlite3.connect('health.db')
    cursor = conn.cursor()

    user_id = session['user_id']

    # USER STREAKS

    cursor.execute(
    "SELECT smoke_streak, alcohol_streak FROM users WHERE id=?",
    (user_id,)
    )

    data = cursor.fetchone()

    smoke_streak = data[0]
    alcohol_streak = data[1]

    # LATEST USER ACTIVITY

    cursor.execute(
    "SELECT * FROM habits WHERE user_id=? ORDER BY id DESC LIMIT 1",
    (user_id,)
    )

    latest = cursor.fetchone()

    smoking = 0
    alcohol = 0
    sleep = 0
    exercise = 0

    if latest:

        smoking = latest[2]
        alcohol = latest[3]
        sleep = latest[4]
        exercise = latest[5]

    # HEALTH ANALYSIS

    health_status = ""
    risk_level = ""
    suggestion = ""

    # SMOKING

    if smoking >= 20:
        health_status += "⚠ Extremely high smoking detected.<br>"
        risk_level = "High Risk"

    elif smoking >= 10:
        health_status += "⚠ Smoking level is unhealthy.<br>"
        risk_level = "Moderate Risk"

    elif smoking > 0:
        health_status += "⚠ Try reducing smoking gradually.<br>"
        risk_level = "Low Risk"

    else:
        health_status += "✅ Smoke-free lifestyle maintained.<br>"
        risk_level = "Healthy"

    # ALCOHOL

    if alcohol >= 8:
        health_status += "⚠ Alcohol intake is very high.<br>"

    elif alcohol >= 4:
        health_status += "⚠ Reduce alcohol consumption.<br>"

    elif alcohol == 0:
        health_status += "✅ Alcohol-free streak maintained.<br>"

    # SLEEP

    if sleep < 5:
        health_status += "⚠ Very poor sleep cycle.<br>"

    elif sleep < 7:
        health_status += "⚠ Sleep quality needs improvement.<br>"

    else:
        health_status += "✅ Healthy sleep cycle maintained.<br>"

    # EXERCISE

    if exercise < 10:
        health_status += "⚠ Very low physical activity.<br>"

    elif exercise < 30:
        health_status += "⚠ Increase daily exercise.<br>"

    else:
        health_status += "✅ Good exercise consistency.<br>"

    # FINAL SUGGESTIONS

    suggestion = '''
    ✔ Drink more water<br>
    ✔ Maintain proper sleep schedule<br>
    ✔ Reduce smoking slowly<br>
    ✔ Exercise daily for better recovery
    '''

    conn.close()

    return render_template(
    'dashboard.html',

    smoke_streak=smoke_streak,
    alcohol_streak=alcohol_streak,

    smoking=smoking,
    alcohol=alcohol,
    sleep=sleep,
    exercise=exercise,

    health_status=health_status,
    risk_level=risk_level,
    suggestion=suggestion
    )

# ADD DATA

@app.route('/add_data', methods=['POST'])
def add_data():

    smoking = int(request.form['smoking'])
    alcohol = int(request.form['alcohol'])
    sleep = float(request.form['sleep'])
    exercise = int(request.form['exercise'])

    today = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect('health.db')
    cursor = conn.cursor()

    user_id = session['user_id']

    cursor.execute(
    '''
    INSERT INTO habits(
    user_id,
    smoking,
    alcohol,
    sleep,
    exercise,
    date
    )
    VALUES(?,?,?,?,?,?)
    ''',
    (
    user_id,
    smoking,
    alcohol,
    sleep,
    exercise,
    today
    )
    )

    cursor.execute(
    "SELECT smoke_streak, alcohol_streak FROM users WHERE id=?",
    (user_id,)
    )

    streaks = cursor.fetchone()

    smoke_streak = streaks[0]
    alcohol_streak = streaks[1]

    if smoking == 0:
        smoke_streak += 1
    else:
        smoke_streak = 0

    if alcohol == 0:
        alcohol_streak += 1
    else:
        alcohol_streak = 0

    cursor.execute(
    '''
    UPDATE users
    SET smoke_streak=?, alcohol_streak=?
    WHERE id=?
    ''',
    (
    smoke_streak,
    alcohol_streak,
    user_id
    )
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

# HISTORY

@app.route('/history')
def history():

    conn = sqlite3.connect('health.db')
    cursor = conn.cursor()

    user_id = session['user_id']

    cursor.execute(
    "SELECT * FROM habits WHERE user_id=? ORDER BY id DESC",
    (user_id,)
    )

    habits = cursor.fetchall()

    conn.close()

    return render_template(
    'history.html',
    habits=habits
    )

# ANALYTICS

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# GOALS

@app.route('/goals')
def goals():
    return render_template('goals.html')

# PROFILE

@app.route('/profile')
def profile():

    conn = sqlite3.connect('health.db')
    cursor = conn.cursor()

    user_id = session['user_id']

    cursor.execute(
    "SELECT username,email,smoke_streak,alcohol_streak FROM users WHERE id=?",
    (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template(
    'profile.html',
    username=user[0],
    email=user[1],
    smoke_streak=user[2],
    alcohol_streak=user[3]
    )

# LOGOUT

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=3000)