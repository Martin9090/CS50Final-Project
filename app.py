import os
import csv
import io

from cs50 import SQL
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    send_file,
)
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, datetime_change, calculate_age, time

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["datetime_change"] = datetime_change
app.jinja_env.filters["calculate_age"] = calculate_age
app.jinja_env.filters["time"] = time

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/patients")
@login_required
def patients():
    """Disply Patients"""
    # get patient list from database for current user
    patients = db.execute("SELECT * FROM patient WHERE user_id = ?", session["user_id"])
    # Rneder patients page passing in patient data for use on page
    return render_template("patients.html", patients=patients)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/patients")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure second password was submitted
        elif request.form.get("password") != request.form.get(
            "confirmation"
        ) or not request.form.get("password"):
            return apology("password does not match", 400)

        # Hash password
        hashed = generate_password_hash(
            request.form.get("password"), method="pbkdf2:sha256", salt_length=16
        )

        # Insert username and password into database and check for already used username
        try:
            db.execute(
                "INSERT INTO users (username, hash) values (?, ?)",
                request.form.get("username"),
                hashed,
            )
        except ValueError:
            return apology("username already taken", 400)
        # message flashing to show successful
        flash("Registered!")
        return redirect("/patients")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """change password"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide new password", 400)

        # Ensure second password was submitted
        elif request.form.get("password") != request.form.get(
            "confirmation"
        ) or not request.form.get("password"):
            return apology("password does not match", 400)

        # Query database for current password
        password = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
        print(password)

        # check current password is correct
        if not check_password_hash(
            password[0]["hash"], request.form.get("current_password")
        ):
            return apology("invalid current password", 400)

        # Hash new password
        hashed = generate_password_hash(
            request.form.get("password"), method="pbkdf2:sha256", salt_length=16
        )

        # update user passowrd in databse
        db.execute("UPDATE users SET hash =? WHERE id =?", hashed, session["user_id"])

        # message flashing to show successful
        flash("Password Changed!")

        return redirect("/patients")

    else:
        return render_template("account.html")


@app.route("/")
# @login_required
def homepage():
    """Homepage"""

    return render_template("homepage.html")


@app.route("/add_patient", methods=["GET", "POST"])
@login_required
def add_patient():
    """Add new patient"""
    if request.method == "POST":
        # Ensure name was submitted
        if not request.form.get("patient_name"):
            return apology("must provide patient name", 400)
        # Ensure date of birth was submitted
        elif not request.form.get("dob"):
            return apology("must provide age", 400)
        # Ensure height was submitted
        elif not request.form.get("height"):
            return apology("must provide height", 400)
        # Ensure weight was submitted
        elif not request.form.get("weight"):
            return apology("must provide weight", 400)

        # Check if patient name already in use for this user
        if db.execute(
            "SELECT * FROM patient WHERE name = ? AND user_id = ?",
            request.form.get("patient_name"),
            session["user_id"],
        ):
            return apology("name already in use for this user", 400)
        # Insert patient into database
        db.execute(
            "INSERT INTO patient (name, age, height, weight, user_id) values (?, ?, ?, ?, ?)",
            request.form.get("patient_name"),
            request.form.get("dob"),
            request.form.get("height"),
            request.form.get("weight"),
            session["user_id"],
        )
        # message flashing to show successful
        flash("Patient Registered!")

        return redirect("/patients")

    else:
        return render_template("add_patient.html")


@app.route("/graph", methods=["GET", "POST"])
@login_required
def graph():
    """Show history of selected patient temps in a graph format"""
    if request.method == "POST":
        # check if patient submitted
        if not request.form.get("patient"):
            return apology("missing patient", 400)
        # get patient id from patient
        patient_id = db.execute(
            "SELECT id FROM patient WHERE name = ?", request.form.get("patient")
        )
        # Get anme of patient from form
        name = request.form.get("patient")
        # Get temperature data from database for patient.
        temp_data = db.execute(
            "SELECT * FROM (SELECT selected_time, temp FROM temp WHERE patient_id = ? AND user_id = ? ORDER BY selected_time DESC LIMIT 10) t1 ORDER BY selected_time",
            patient_id[0]["id"],
            session["user_id"],
        )
        # check if there is any temperature data
        if not temp_data:
            return apology("no temperature data", 400)
        # Create empty lists for graph information
        dates = []
        temps = []
        # Loop through temp data adding temperature to temp and dates to dates lists
        for result in temp_data:
            dates.append(datetime_change(result["selected_time"]))
            temps.append(result["temp"])
        # Render graph page passing in dates, temps and name for use on page
        return render_template("graphone.html", dates=dates, temps=temps, name=name)
    else:
        # Get patient names from database for user to use in dropdown name selection
        patient = db.execute(
            "SELECT name FROM patient WHERE user_id = ?", session["user_id"]
        )
        # Render page passing in patient data for use on page
        return render_template("graph.html", patients=patient)


@app.route("/temperature", methods=["GET", "POST"])
@login_required
def temperature():
    if request.method == "POST":
        # check if patient submitted
        if not request.form.get("patient"):
            return apology("missing patient", 400)
        # check if temperature submitted
        if not request.form.get("temperature"):
            return apology("missing temperature", 400)
        # check that a date time has been selected
        if not request.form.get("time_taken"):
            return apology("missing date and time", 400)
        # get patient id from patient
        patient_id = db.execute(
            "SELECT id FROM patient WHERE name = ?", request.form.get("patient")
        )
        # Insert temperature data into database
        # In this and other tables I have included the current data and time as well
        # the user selected date and time to allow for background checking of input data
        db.execute(
            "INSERT INTO temp (patient_id, user_id, current_time, selected_time, temp) values (?, ?, ?, ?, ?)",
            patient_id[0]["id"],
            session["user_id"],
            time(),
            request.form.get("time_taken"),
            request.form.get("temperature"),
        )

        # message flashing to show successful
        flash("Temperature Registered!")
        # Redirect to temperature reloading page
        return redirect("/temperature")
    else:
        """Display last 10 temperature readings input sorted by user given date latest first"""
        # Get all patient names for current user to use in dropdown
        patient = db.execute(
            "SELECT name FROM patient WHERE user_id = ?", session["user_id"]
        )
        # Get data from temp table and sort by the the 10 most recent.
        temps = db.execute(
            "SELECT patient.name, users.username, temp.selected_time, temp.temp FROM ((temp "
            "INNER JOIN users ON temp.user_id = users.id)"
            "INNER JOIN patient ON temp.patient_id = patient.id) "
            "WHERE users.id = ? "
            "ORDER BY selected_time DESC LIMIT 10",
            session["user_id"],
        )
        # Render page passing in patinet and temp data for use.
        return render_template("temperature.html", patients=patient, temps=temps)


@app.route("/medication/", methods=["GET", "POST"])
@login_required
def medication():
    if request.method == "POST":
        """Record medication given to patient"""
        # check if patient submitted
        if not request.form.get("patient"):
            return apology("missing patient", 400)
        # check if medication submitted
        if not request.form.get("medication"):
            return apology("missing medication", 400)
        # check if amount submitted
        if not request.form.get("amount_given"):
            return apology("missing amount given", 400)
            # check that a date time has been selected
        if not request.form.get("time_taken"):
            return apology("missing date and time", 400)
        # get patient id from patient
        patient_id = db.execute(
            "SELECT id FROM patient WHERE name = ? AND user_id = ?",
            request.form.get("patient"),
            session["user_id"],
        )

        # Concatenating the amount and doasge together to use as a single entry for database
        given_medication = (
            request.form.get("amount_given") + " " + request.form.get("dosage")
        )
        # Insert medication data into database
        db.execute(
            "INSERT INTO medication (patient_id, user_id, current_time, selected_time, medication, dosage) values (?, ?, ?, ?, ?, ?)",
            patient_id[0]["id"],
            session["user_id"],
            time(),
            request.form.get("time_taken"),
            request.form.get("medication"),
            given_medication,
        )

        # message flashing to show successful
        flash("Medication Registered!")
        # Redirect to medication reloading page
        return redirect("/medication/")
    else:
        """Display last 10 medications given sorted by user given date most recent first"""
        # Get all patient names for current user to use in dropdown
        patient = db.execute(
            "SELECT name FROM patient WHERE user_id = ?", session["user_id"]
        )
        # Get data from medication table and sort by the the 10 most recent.
        meds = db.execute(
            "SELECT patient.name, users.username, medication.selected_time, medication.medication, medication.dosage "
            "FROM ((medication INNER JOIN users ON medication.user_id = users.id) "
            "INNER JOIN patient ON medication.patient_id = patient.id) "
            "WHERE users.id = ? ORDER BY selected_time DESC LIMIT 10",
            session["user_id"],
        )
        # Render medication page passing in patient and medication data for use
        return render_template("medication.html", patients=patient, meds=meds)


@app.route("/symptoms", methods=["GET", "POST"])
@login_required
def symptoms():
    """Record symptoms of patient"""
    if request.method == "POST":
        # check if patient submitted
        if not request.form.get("patient"):
            return apology("missing patient", 400)
        # check if symptom submitted
        if not request.form.get("symptom"):
            return apology("missing symptom", 400)
        # check that a date time has been selected
        if not request.form.get("time_taken"):
            return apology("missing date and time", 400)
        # get patient id from patient
        patient_id = db.execute(
            "SELECT id FROM patient WHERE name = ?", request.form.get("patient")
        )
        # Insert symptoms data into database
        db.execute(
            "INSERT INTO symptom (patient_id, user_id, current_time, selected_time, symptom) values (?, ?, ?, ?, ?)",
            patient_id[0]["id"],
            session["user_id"],
            time(),
            request.form.get("time_taken"),
            request.form.get("symptom"),
        )

        # message flashing to show successful
        flash("Symptoms Registered!")
        # Redirect back to symptoms page
        return redirect("/symptoms")

    else:
        """Display last 10 symptoms entered sorted by user given date most recent first"""
        # Get all patient names for current user to use in dropdown
        patient = db.execute(
            "SELECT name FROM patient WHERE user_id = ?", session["user_id"]
        )
        # Get data from symptoms table and sort by the the 10 most recent.
        symptoms = db.execute(
            "SELECT patient.name, users.username, symptom.selected_time, symptom.symptom "
            "FROM ((symptom INNER JOIN users ON symptom.user_id = users.id) "
            "INNER JOIN patient ON symptom.patient_id = patient.id) "
            "WHERE users.id = ? "
            "ORDER BY selected_time DESC LIMIT 10",
            session["user_id"],
        )
        # Render symptoms page passing in patient and symptoms data for use
        return render_template("symptoms.html", patients=patient, symptoms=symptoms)


@app.route("/links")
@login_required
def links():
    # Render links page
    return render_template("links.html")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    """Select patient to update data"""
    if request.method == "POST":
        # check if patient submitted
        if not request.form.get("patient"):
            return apology("missing patient", 400)
        # get patient data from patient database for user
        patient_data = db.execute(
            "SELECT * FROM patient WHERE name = ? AND user_id = ?",
            request.form.get("patient"),
            session["user_id"],
        )
        # Render updateone page passing data for use
        return render_template("updateone.html", patient_data=patient_data)
    else:
        # Get all patient names for current user to use in dropdown
        patient = db.execute(
            "SELECT name FROM patient WHERE user_id =?",
            session["user_id"],
        )
        # Render update page passing in patient data for use
        return render_template("update.html", patients=patient)


@app.route("/updateone", methods=["POST"])
@login_required
def updateone():
    """Update patient data"""
    # check if patient date of birth submitted
    if not request.form.get("dob"):
        return apology("must provide age", 400)
    # check if patient height submitted
    elif not request.form.get("height"):
        return apology("must provide height", 400)
    # check if patient weight submitted
    elif not request.form.get("weight"):
        return apology("must provide weight", 400)
    # Update patient data in database
    db.execute(
        "UPDATE patient SET age = ?, height = ?, weight = ? WHERE name = ? AND user_id = ?",
        request.form.get("dob"),
        request.form.get("height"),
        request.form.get("weight"),
        request.form.get("name"),
        session["user_id"],
    )
    # message flashing to show successful
    flash("Patient Data Updated!")
    # Redirect to patient page
    return redirect("/patients")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Delete patient data"""
    if request.method == "POST":
        # Ensure patient name was submitted
        if not request.form.get("patient_name"):
            return apology("must provide patient name", 400)
        # Get patient id from patient database for user and save in variable for checking
        patient_id = db.execute(
            "SELECT id FROM patient WHERE name = ? AND user_id = ?",
            request.form.get("patient_name"),
            session["user_id"],
        )
        # Check if patient variable is empty if it is give error.
        # Popup tooltip added to patient name field on delete page explaining name
        # s case sensitive to hopefully avoid accidental deletion and give instruction
        if not patient_id:
            return apology("check patient name", 400)
        # Delete all user data table by table and then deleting user from patient table
        db.execute(
            "DELETE FROM temp WHERE patient_id = ? AND user_id =?",
            patient_id[0]["id"],
            session["user_id"],
        )
        db.execute(
            "DELETE FROM symptom WHERE patient_id = ? AND user_id =?",
            patient_id[0]["id"],
            session["user_id"],
        )
        db.execute(
            "DELETE FROM medication WHERE patient_id = ? AND user_id =?",
            patient_id[0]["id"],
            session["user_id"],
        )
        db.execute(
            "DELETE FROM patient WHERE id = ? AND user_id =?",
            patient_id[0]["id"],
            session["user_id"],
        )

        # message flashing to show successful
        flash("Patient Data DELETED!")
        # Redirect to delete page
        return redirect("/patients")

    else:
        # Render delete page
        return render_template("delete.html")


# when making the donwload function I did need to AI (chatGPT)
# in order to get it working as i wanted it with the output
# layout of the csv file
@app.route("/download", methods=["GET", "POST"])
@login_required
def download():
    """Download all patient data"""
    if request.method == "POST":
        # check if patient submitted
        if not request.form.get("patient"):
            return apology("missing patient", 400)
        # get patient id from patient for user
        patient_id = db.execute(
            "SELECT id FROM patient WHERE name = ? AND user_id = ?",
            request.form.get("patient"),
            session["user_id"],
        )
        # get patient data from patient table
        patient_data = db.execute(
            "SELECT name, age, height, weight FROM patient WHERE id = ? AND user_id = ?",
            patient_id[0]["id"],
            session["user_id"],
        )
        # get patient data from temp table
        temp_data = db.execute(
            "SELECT selected_time AS time_taken, temp FROM temp WHERE patient_id = ? AND user_id = ? ORDER BY selected_time DESC",
            patient_id[0]["id"],
            session["user_id"],
        )
        # get patient data from symptom table
        symptom_data = db.execute(
            "SELECT selected_time AS time, symptom FROM symptom WHERE patient_id = ? AND user_id = ? ORDER BY selected_time DESC",
            patient_id[0]["id"],
            session["user_id"],
        )
        # get patient data from medication table
        medication_data = db.execute(
            "SELECT selected_time AS time_given, medication, dosage FROM medication WHERE patient_id = ? AND user_id = ? ORDER BY selected_time DESC",
            patient_id[0]["id"],
            session["user_id"],
        )
        # Create dicitonary of the headers to be used in the csv file creation
        fieldnames = [
            {"header": ["name", "age", "height", "weight"], "data": patient_data},
            {"header": ["time_taken", "temp"], "data": temp_data},
            {"header": ["time", "symptom"], "data": symptom_data},
            {"header": ["time_given", "medication", "dosage"], "data": medication_data},
        ]
        # create CSV entirely in memory to avoid filesystem locks
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[])

        for names in fieldnames:
            writer.fieldnames = names["header"]
            writer.writeheader()

            for row in names["data"]:
                row_headers = {key: row.get(key, "") for key in writer.fieldnames}
                writer.writerow(row_headers)

        csv_text = output.getvalue()
        output.close()

        try:
            return send_file(
                io.BytesIO(csv_text.encode("utf-8")),
                as_attachment=True,
                download_name="patient_data.csv",
                mimetype="text/csv",
            )
        except Exception as e:
            return apology(f"Error occured: {e}", 500)
    else:
        """Select patient to download data"""
        # Get patient date from patient table for user to use in dropdown name selection
        patient = db.execute(
            "SELECT name FROM patient WHERE user_id = ?", session["user_id"]
        )
        # Render download page and pass in patient data
        return render_template("download.html", patients=patient)


# From the patients page each patient has a dashboard button next to them that will
# send them to the dashboard page while also passing in the patient id number this allows
# the use of that id to display the tables and graph without having to select the user
# again or when updating any of the tables.
@app.route("/dashboard/<patient_id>", methods=["GET"])
@login_required
def getDashboard(patient_id):
    """Patient dashboard showing cut down versions of all information"""
    # Get patient data from database
    patient = db.execute(
        "SELECT * FROM patient WHERE id = ? and user_id = ?",
        patient_id,
        session["user_id"],
    )
    # Get patient temperature data from database for user order by 5 most recent
    temperatures = db.execute(
        "SELECT * FROM temp WHERE patient_id = ? AND user_id = ? order by selected_time DESC LIMIT 5",
        patient_id,
        session["user_id"],
    )
    # Get patient medication data from database for user order by 5 most recent
    medication = db.execute(
        "SELECT * FROM medication WHERE patient_id = ? AND user_id = ? order by selected_time DESC LIMIT 5",
        patient_id,
        session["user_id"],
    )
    # Get patient symptom data from database for user order by 5 most recent
    symptoms = db.execute(
        "SELECT * FROM symptom WHERE patient_id = ? AND user_id = ? order by selected_time DESC LIMIT 5",
        patient_id,
        session["user_id"],
    )
    # Lists for graph infromaion
    dates = []
    temps = []

    # Loop through temperatures data and add temperature to temp and dates to dates lists
    for result in temperatures:
        dates.insert(0, (datetime_change(result["selected_time"])))
        temps.insert(0, (result["temp"]))
    # Render dashboard page passing in all data for use
    return render_template(
        "dashboard.html",
        patient=patient,
        temperatures=temperatures,
        medication=medication,
        symptoms=symptoms,
        dates=dates,
        temps=temps,
    )


@app.route("/dashboard/temp", methods=["POST"])
@login_required
def post_temp():
    """Function called when posting temperature on dashboard page"""
    # check if temperature submitted
    if not request.form.get("temperature"):
        return apology("missing temperature", 400)
    # check if date time selected
    if not request.form.get("time_taken"):
        return apology("missing date and time", 400)

    # get hidden patient id from dashboard page
    patient_id = request.form.get("patient_id")

    # Insert temperature data into database
    db.execute(
        "INSERT INTO temp (patient_id, user_id, current_time, selected_time, temp) values (?, ?, ?, ?, ?)",
        patient_id,
        session["user_id"],
        time(),
        request.form.get("time_taken"),
        request.form.get("temperature"),
    )

    # message flashing to show successful
    flash("Temperature Registered!")
    # Redirect to dashboard reloading page with patient id
    return redirect("/dashboard/" + str(patient_id))


@app.route("/dashboard/medication", methods=["POST"])
@login_required
def post_meds():
    """Function called when posting medication on dashboard page"""
    if not request.form.get("medication"):
        return apology("missing medication", 400)
    # check if amount submitted
    if not request.form.get("amount_given"):
        return apology("missing amount given", 400)
    # check if date time selected
    if not request.form.get("time_taken"):
        return apology("missing date and time", 400)

    # get hidden patient id from dashboard page
    patient_id = request.form.get("patient_id")

    # Concatenating the amount and doasge together to use as a single entry for database
    given_medication = (
        request.form.get("amount_given") + " " + request.form.get("dosage")
    )
    # Insert medication data into database
    db.execute(
        "INSERT INTO medication (patient_id, user_id, current_time, selected_time, medication, dosage) values (?, ?, ?, ?, ?, ?)",
        patient_id,
        session["user_id"],
        time(),
        request.form.get("time_taken"),
        request.form.get("medication"),
        given_medication,
    )
    # message flashing to show successful
    flash("Medication Registered!")

    # Redirect to dashboard reloading page with patient id
    return redirect("/dashboard/" + str(patient_id))


@app.route("/dashboard/symptoms", methods=["POST"])
@login_required
def post_symptom():
    """Function called when posting symptom on dashboard page"""
    # check if symptom submitted
    if not request.form.get("symptom"):
        return apology("missing symptom", 400)
    # check if date time selected
    if not request.form.get("time_taken"):
        return apology("missing date and time", 400)

    # get hidden patient id from dashboard page
    patient_id = request.form.get("patient_id")

    # Insert symptom data into database
    db.execute(
        "INSERT INTO symptom (patient_id, user_id, current_time, selected_time, symptom) values (?, ?, ?, ?, ?)",
        patient_id,
        session["user_id"],
        time(),
        request.form.get("time_taken"),
        request.form.get("symptom"),
    )

    # message flashing to show successful
    flash("Symptom Registered!")

    # Redirect to dashboard reloading page with patient id
    return redirect("/dashboard/" + str(patient_id))


@app.route("/dashboard/csv", methods=["POST"])
@login_required
def dashboard_csv():
    """Create and offer for download csv file off all user data"""
    # get patient id from patient for user
    patient_id = db.execute(
        "SELECT id FROM patient WHERE id = ?AND user_id = ?",
        request.form.get("patient_id"),
        session["user_id"],
    )
    # get patient data from patient table
    patient_data = db.execute(
        "SELECT name, age, height, weight FROM patient WHERE id = ? AND user_id = ?",
        patient_id[0]["id"],
        session["user_id"],
    )
    # get patient data from temp table
    temp_data = db.execute(
        "SELECT selected_time AS time_taken, temp FROM temp WHERE patient_id = ? AND user_id = ? ORDER BY selected_time DESC",
        patient_id[0]["id"],
        session["user_id"],
    )
    # get patient data from symptom table
    symptom_data = db.execute(
        "SELECT selected_time AS time, symptom FROM symptom WHERE patient_id = ? AND user_id = ? ORDER BY selected_time DESC",
        patient_id[0]["id"],
        session["user_id"],
    )
    # get patient data from medication table
    medication_data = db.execute(
        "SELECT selected_time AS time_given, medication, dosage FROM medication WHERE patient_id = ? AND user_id = ? ORDER BY selected_time DESC",
        patient_id[0]["id"],
        session["user_id"],
    )
    # Create dicitonary of the headers to be used in the csv file creation
    fieldnames = [
        {"header": ["name", "age", "height", "weight"], "data": patient_data},
        {"header": ["time_taken", "temp"], "data": temp_data},
        {"header": ["time", "symptom"], "data": symptom_data},
        {"header": ["time_given", "medication", "dosage"], "data": medication_data},
    ]
    # create csv file and name it and headers to use
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[])

    for names in fieldnames:
        writer.fieldnames = names["header"]
        writer.writeheader()

        for row in names["data"]:
            row_headers = {key: row.get(key, "") for key in writer.fieldnames}
            writer.writerow(row_headers)

    csv_text = output.getvalue()
    output.close()

    try:
        return send_file(
            io.BytesIO(csv_text.encode("utf-8")),
            as_attachment=True,
            download_name="patient_data.csv",
            mimetype="text/csv",
        )
    except Exception as e:
        return apology(f"Error occured: {e}", 500)
