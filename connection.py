from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pass@2023",
    database="hospital"
)

# Route for home.html
@app.route('/')
def home():
    return render_template('home.html')

# Route for records.html
@app.route('/records')
def records():
    conn = db
    cur = conn.cursor()

    # Fetch patient data
    cur.execute("SELECT patient_id, first_name, last_name, gender, county, age FROM patients")
    patients = cur.fetchall()

    # Fetch next of kin data
    cur.execute("SELECT patient_id, first_name, surname, relationship FROM next_of_kin")
    next_of_kin = cur.fetchall()

    return render_template('records.html', patients=patients, next_of_kin=next_of_kin)

# Route for registration.html
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Check which form was submitted
        if 'name' in request.form:  # Patient registration form
            first_name = request.form['name']
            last_name = request.form.get('last_name', '')  # Add a field for last name
            email = request.form['email']
            gender = request.form['gender']
            county = request.form['county']
            age = request.form.get('age', None)  # Add a field for age

            # Insert patient data into the database
            cursor = db.cursor()
            try:
                cursor.execute(
                    "INSERT INTO patients (first_name, last_name, email, gender, county, age) VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, email, gender, county, age)
                )
                db.commit()
                flash('Patient registered successfully!', 'success')
            except Exception as e:
                db.rollback()
                flash(f'Error: {e}', 'danger')

        elif 'patient_id' in request.form:  # Next of kin registration form
            patient_id = request.form['patient_id']
            first_name = request.form['first_name']
            surname = request.form['surname']
            relationship = request.form['relationship']

            # Insert next-of-kin data into the database
            cursor = db.cursor()
            try:
                cursor.execute(
                    "INSERT INTO next_of_kin (patient_id, first_name, surname, relationship) VALUES (%s, %s, %s, %s)",
                    (patient_id, first_name, surname, relationship)
                )
                db.commit()
                flash('Next of Kin registered successfully!', 'success')
            except Exception as e:
                db.rollback()
                flash(f'Error: {e}', 'danger')

        return redirect(url_for('registration'))

    return render_template('registration.html')

if __name__ == '__main__':
    app.run(debug=True)
