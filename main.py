from flask import Flask, render_template, request, redirect, flash, session
import pymongo
from pymongo import MongoClient
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
            flash("Email not found", "error")      
            return redirect('/')
        else:
            if(checkingPassword(password, password_finder(email))):
                session["name"] = user_finder(email)         # These two lines of code are needed for presenting a table with the user information in the logged_in page. Check the logged_in function (you will see that both name and email are needed).
                session["email"] = email                   
                return redirect('/logged_in')
            else:
                flash("Wrong password", "error")         
                return redirect('/')
    else:
        return render_template('login.html')


@app.route('/subscribe.html', methods=['GET', 'POST']) 
def subscribe():
    
    if request.method =='POST':
        name = request.form['username']
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
            flash("Try with another email: the email is already stored", "error")   
            return redirect('/subscribe.html')
        else:
            data = {"name": name,
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

            new_keys = []
            new_values = []
            for key, value in data.items():
                if value != "":
                    new_keys.append(key)
                    new_values.append(value)
            fixed_data = dict(zip(new_keys,new_values)) #dictionary without items that present an empty value 

            collection.insert_one(fixed_data)
        return redirect('/greet')

    else:
        return render_template('/subscribe.html')

@app.route('/logged_in')
def logged_in():
    if 'name' in session:            # If a right email and a right password have not already been used, then there won't be a name in the session.
        doc = data_finder(session["email"])                 
        return render_template("logged_in.html", doc = doc) 
    else:
        flash("Please first Login!", "error")         
        return redirect('/')


@app.route("/logout")
def logout():
    session.pop("name", None) # This remove the name and placed instead of it "None".
    # It is important because when someone press the logout button, then the session with its name should not be accessible, by typing the path, anymore.
    return redirect("/")

@app.route('/greet')
def greet():
    return render_template("greet.html")

def email_is_already_stored(email):
    '''Returns True if email is already in the database, False if not'''
    return collection.find_one({"email": email}) != None   
# collection.find_one({"email": email}) returns the email if it is in the database and returns None if there isn't.
# Therefore, if the email is in the database the result is for example Adriano@Ettari.it == None and so 
# collection.find_one({"email": email}) == None  returns False. So not(False)=True. So, if the email is in the
# database, this function returns True.

def user_finder(email): 
    '''Returns the username stored according to the email inserted'''
    cur = collection.find({"email": email})   # Since we use .find and not .find_one, the result is a cursor
    # that basically returns all the dictionaries with the email equal to the email we selected.
    for doc in cur:  
        return doc["user"]

def password_finder(email):
    '''Returns the hashed password stored according to the email inserted'''
    cur = collection.find({"email": email})
    for doc in cur:
        rescued_hashed_password = doc["ps"]
    cur.close()
    return rescued_hashed_password

def data_finder(email): 
    '''Returns all the user information but id and pw'''
    cur = collection.find({"email": email}) 
    for doc in cur:
        data_found = doc
    del data_found["_id"]   
    del data_found["ps"]    
    cur.close()
    return data_found
    


if __name__ == "__main__":
    app.secret_key = 'qwerty1234'
    app.run(debug=True)