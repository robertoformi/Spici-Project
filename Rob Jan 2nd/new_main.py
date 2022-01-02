from flask import Flask, render_template, request, redirect, flash, session
import pymongo
from pymongo import MongoClient
import bcrypt
from crypting import checkingPassword, codingPassword

cluster = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = cluster["spici_project"]
collection = db["business_data"] 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method =='POST':
        email = request.form['email']
        password = request.form['pw']

        if not(email_is_already_stored(email)):
            flash("Email not found", "error")      # HERE
            return redirect('/')
        else:
            if(checkingPassword(password, password_finder(email))):
                session["name"] = user_finder(email)
                session["email"] = email                   # HERE
                return redirect('/logged_in')
            else:
                flash("Wrong password", "error")         # HERE
                return redirect('/')
    else:
        return render_template('loginX.html')


@app.route('/Megasub.html', methods = ['GET', 'POST']) 
def subscribe():
    
    if request.method =='POST':

        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        ps1 = request.form['password1']
        ps2 = request.form['password2']
        age = request.form['age']

        fiscal_Code = request.form['fiscal_code']
        phone_num = request.form['phone_num']
        company_name = request.form['company_name']
        purpose = request.form['purpose']
        date_foundation = request.form['date_foundation']
        city = request.form['city']
        street = request.form['street']
        zip = request.form['zip']
        share_capital = request.form['share_capital']
        vat = request.form['vat']


        if email_is_already_stored(email):
            flash("Try with another email: the email is already stored", "error")   # HERE
            return redirect('/Megasub.html')
        else:
            dato1 = {"name": name,
                    "surname": surname,
                    "email": email, 
                    "ps": codingPassword(ps1),
                    "age": age,
                    "fiscal_code": fiscal_Code,
                    "phone_num": phone_num,
                    "company_name": company_name,
                    "purpose": purpose,
                    "date_foundation": date_foundation,
                    "city": city,
                    "street": street,
                    "zip": zip,
                    "share_capital": share_capital,
                    "vat": vat,
                    }
                    
            collection.insert_one(dato1)
        return redirect('/greet')

    else:
        return render_template('/MegaSub.html')

@app.route('/logged_in')
def logged_in():

    if 'name' in session:
        doc = data_finder(session["email"])
        return render_template("logged_in.html", doc = doc)  # HERE
    else:
        flash("Please login first!", "error")         # HERE
        return redirect('/')

# @app.route('/error_page')                  HERE
# def error_page():
#     return render_template("error_page.html")

@app.route("/logout")
def logout():
    session.pop("name",None)
    return redirect("/")

@app.route('/greet')
def greet():
    return render_template("greet.html")

def email_is_already_stored(email):
    '''returns True if email is already in the database, False if not'''
    return not(db.spici_project.find_one({"email": email}) == None)

def user_finder(email):                                 # HERE
    '''returns user stored for the email inserted'''
    cur = db.spici_project.find({"email": email})
    for doc in cur:
        return doc["user"]

def password_finder(email):
    '''returns hashed password stored for the email inserted'''
   
    cur = db.spici_project.find({"email": email})
    for doc in cur:
        rescued_hashed_password = doc["ps"]
    cur.close()
    return rescued_hashed_password

def data_finder(email):                               # HERE
    '''
    Returns user information without id and pw
    '''
    cur = db.business_data.find({"email": email}) 
    for doc in cur:
        data_found = doc
    del data_found["_id"]   # HERE
    del data_found["ps"]    # HERE
    cur.close()
    return data_found
    


if __name__ == "__main__":
    app.secret_key = 'qwerty1234'
    app.run(debug=True)