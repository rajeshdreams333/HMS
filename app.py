from flask import *
import random
import sqlite3
from flask import Flask, session
from admin import admin_bp
from patient import patient_bp
app = Flask(__name__)
app.secret_key = 'dev'
# ======================================Creating tables=========================================================
def Create_tables():
    conn=sqlite3.connect('Team_2.db')
    c = conn.cursor()
    conn.execute('''
    create table if not exists patient(
    Patient_Id INTEGER PRIMARY KEY,
    Patient_Name VARCHAR(20),
    Room_No INTEGER,
    Doctor_Id INTEGER,
    Doctor_Name VARCHAR(20),
    Gender VARCHAR(10),
    Patient_Age INTEGER,
    Weight INTEGER,
    Height INTERGER,
    Blood_Group VARCHAR(10),
    Phone_No INTEGER,
    Address VARCHAR(50),
    Email VARCHAR(20)
    )''')
    conn.commit()
    conn.execute('''
    create table if not exists compliants(
    User_Name VARCHAR(20),
    Time VARCHAR(10),
    Date VARCHAR(10),
    Mobile INTEGER,
    Issue_type VARCHAR(20),
    Description VARCHAR(50)
    )''')
    conn.commit()
    conn.close()
Create_tables()
# ============================================================================================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        if role == 'admin':
            if username=="admin" and password=="1234":
                session['username'] = username
                return redirect('/admin/home')
            else:
                return redirect('/admin/home')
        elif role == 'patient':
            l=[]
            con = sqlite3.connect("Team_2.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select Patient_Name from patient")
            q1 = cur.fetchall()
            for i in q1:
                l.append(i['Patient_Name'])
            cur.execute("select Email from patient")
            q2 = cur.fetchall()
            for i in q2:
                l.append(i['Email'])
            if username and password in l:
                session['username']=username
                return redirect('patient/patient_page')
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        return render_template('login.html')
# ===============================================================================================================
app.register_blueprint(admin_bp)
app.register_blueprint(patient_bp)
# =======================================================================================================================================
if __name__ == '__main__':
    app.run(debug=True)
