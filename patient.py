from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
patient_bp = Blueprint('patient', __name__, url_prefix='/patient')
@patient_bp.route('/patient_page')
def patient_page():
        return render_template('p_home.html')

@patient_bp.route('/services')
def service():
    return render_template('./Patient/services.html')
@patient_bp.route('/issue')
def issue():
    return render_template('./Patient/issues.html')

@patient_bp.route('/issue_submit',methods=['POST','GET'])
def issue_submit():
    if request.method=='POST':
        try:
            username=request.form.get('username')
            date=request.form.get('date')
            time=request.form.get('time')
            mobile=request.form.get('mobile')
            issue_type=request.form.get('issue_type')
            desc=request.form.get('issue')
            print(username,date,time,mobile,issue_type,desc)
            with sqlite3.connect('Team_2.db') as con:
                cur = con.cursor()
                cur.execute("insert into compliants values(?,?,?,?,?,?)", (
                username,date,time,mobile,issue_type,desc))
                con.commit()
        except:
            con.rollback()
        finally:
            return redirect(url_for('patient.issue'))
            con.close()

@patient_bp.route('/profile')
def profile():
    if 'username' in session:
        con = sqlite3.connect("Team_2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(("select * from patient where Patient_Name=?"), (session['username'],))
        rows = cur.fetchall()
    return render_template('./Patient/profile.html', rows = rows)


@patient_bp.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")
