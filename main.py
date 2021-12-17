from flask import Flask, render_template, request, redirect, url_for
import pymongo
from pymongo import MongoClient
import bcrypt
from crypting import checkingPassword, codingPassword


cluster = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = cluster["test"]
collection = db["test"] 

app = Flask(__name__)


@app.route('/', methods =['GET', 'POST'])  # Ask corazza
def login():
    '''
    This function makes the login page work. It checks if the email and the password
    are already in the database or not. In the first case you will be redirected to 
    the logged_in page; in the other case you will be redirected to the error_page.
    '''
    if request.method =='POST':
        email = request.form['email']
        password = request.form['pw']
        
        
        # With db.test_test.find_one({"email": email}) returns the cursor pointing to the first occurence
        # of what you asked in the query {"email":email}.
        # If what you asked is not in the database it returns "None".
        if(db.test.find_one({"email": email}) == None):
            return render_template("error_page.html")
        else:
            # This function returns a cursor pointing to the subset of the database in which each email 
            # matches the email you asked for.
            cur = db.test.find({"email": email})
        # With this for loop you can obtain the each single istance of the database 
        # (tipically we have only one istance for each email).
            for doc in cur:
                rescued_hashed_password = doc["ps"] # with doc["ps"] you obtain only the password stored
        # The following if statement returns true if they are equal and false if they are not
                if not(checkingPassword(password, rescued_hashed_password)):
                    return render_template("error_page.html")
                else:
                    return render_template("logged_in.html") 
    else:
        return render_template("login.html")

# MISSING a function that returns an error if the email you use is already in the database
@app.route('/subscribe.html', methods =['POST','GET']) 
def subscribe():
    if request.method =='POST':
        username = request.form['username']
        surname = request.form['surname']
        email = request.form['email']
        ps1 = request.form['password1']
        ps2 = request.form['password2']
        age = request.form['age']
        
     
        dato1 = {"user": username,
                    "età": age,
                    "cognome": surname,
                    "email": email, 
                    "ps": codingPassword(ps1)
                    }   # Create a library with these items
        collection.insert_one(dato1)  # insert the data into mongo 

        return redirect(url_for('greet', usr = username))
    else:
        return render_template("subscribe.html")

@app.route('/logged_in.html')
def logged_in():
    return render_template("logged_in.html")

@app.route('/<usr>')     # An option for personalised pages (in the link you will what you
# print instead of usr)
def greet(usr):
    return render_template("greet.html", usr = usr)

@app.route('/error_page.html')
def error_page():
    return render_template("error_page.html")


if __name__ == "__main__":
    app.run(debug=True)
