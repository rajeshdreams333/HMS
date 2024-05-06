from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
import random
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
@admin_bp.route('/home')
def admin_page():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
@admin_bp.route('/patient_reg')
def patient_reg():
    n = random.randint(10001, 99999)
    return render_template('./Admin/Patient_reg.html',n=n)

@admin_bp.route('/compliant')
def compliant_page():
    con = sqlite3.connect("Team_2.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from compliants")
    rows = cur.fetchall()
    return render_template("./Admin/Compliant.html", rows=rows)

@admin_bp.route("/savedetails", methods=['POST', 'GET'])
def savedetails():
    if request.method == "POST":
        print("For loop")
        try:
            p_id = request.form.get("p_id")
            p_name = request.form.get("pname")
            room_no = request.form.get("room")
            d_id = request.form.get("d_id")
            d_name = request.form.get("d_name")
            p_gender = request.form.get("gender")
            p_age = request.form.get("age")
            weight = request.form.get("weight")
            height = request.form.get("height")
            blood = request.form.get("bgroup")
            ph_no = request.form.get("mobile")
            address = request.form.get("address")
            email = request.form.get("email")
            print(p_id,p_name,room_no,d_id,d_name,p_gender,p_age,weight,height,blood,ph_no,address,email)
            with sqlite3.connect('Team_2.db') as con:
                cur = con.cursor()
                cur.execute("insert into patient values(?,?,?,?,?,?,?,?,?,?,?,?,?)", (p_id, p_name, room_no, d_id, d_name,  p_gender,p_age, weight, height, blood,ph_no,address,  email,))
                print("hello")
                con.commit()
        except:
            con.rollback()
        finally:
            return redirect(url_for('admin.patient_reg'))
            con.close()
@admin_bp.route('/view')
def view_page():

    con = sqlite3.connect("Team_2.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from patient")
    rows = cur.fetchall()
    return render_template("./Admin/view.html", rows=rows)

@admin_bp.route("/deletebutton", methods=['POST', 'GET'])
def deletePatient():
    if request.method == "GET":
        try:
            id = request.args.get('id')
            with sqlite3.connect('Team_2.db') as con:
                cur = con.cursor()
                q="delete from patient where Patient_Id = ?"
                con.execute(q, (id,))
                con.commit()
        except:
            con.rollback()
        finally:
            return redirect(url_for('admin.view_page'))
            con.close()
# ===========Update Patient Details===================================
@admin_bp.route("/update", methods=['GET'])
def fetchdetails():
    Patient_Id = request.args.get('Patient_Id')
    Patient_Name=request.args.get('Patient_Name')
    Room_No=request.args.get('Room_No')
    Doctor_Id=request.args.get('Doctor_Id')
    Doctor_Name = request.args.get('Doctor_Name')
    Gender = request.args.get('Gender')
    Patient_Age = request.args.get('Patient_Age')
    Weight = request.args.get('Weight')
    Height = request.args.get('Height')
    Blood_Group = request.args.get('Blood_Group')
    Phone_No = request.args.get('Phone_No')
    Address = request.args.get('Address')
    Email = request.args.get('Email')
    return render_template('./Admin/update.html', Patient_Id=Patient_Id, Patient_Name=Patient_Name, Room_No=Room_No, Doctor_Id=Doctor_Id, Doctor_Name=Doctor_Name, Gender=Gender,Patient_Age=Patient_Age,  Weight=Weight, Height=Height, Blood_Group=Blood_Group,Phone_No=Phone_No, Address=Address,  Email=Email)

@admin_bp.route("/updatedetails", methods=['POST','GET'])
def updatePatient():
    if request.method == 'POST':
        try:
            Patient_Id = request.form["Patient_Id"]
            Patient_Name=request.form["Patient_Name"]
            Room_No=request.form["Room_No"]
            Doctor_Id=request.form["Doctor_Id"]
            Doctor_Name = request.form["Doctor_Name"]
            Gender = request.form["Gender"]
            Patient_Age = request.form["Patient_Age"]
            Weight = request.form["Weight"]
            Height = request.form["Height"]
            Blood_Group = request.form["Blood_Group"]
            Phone_No = request.form["Phone_No"]
            Address = request.form["Address"]
            Email = request.form["Email"]
            with sqlite3.connect('Team_2.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE patient SET Patient_Name = ?, Room_No=? ,Doctor_Id=? ,Doctor_Name=? ,Gender=?, Patient_Age=? ,Weight=?, Height=?, Blood_Group=?,Phone_No=?, Address=?, Email=?  where Patient_Id = ?", (Patient_Name, Room_No,Doctor_Id, Doctor_Name,Gender,Patient_Age, Weight, Height, Blood_Group, Phone_No,Address, Email, Patient_Id, ))
                con.commit()
        except:
            con.rollback()
        finally:
            return redirect(url_for('admin.view_page'))
            con.close()

@admin_bp.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")