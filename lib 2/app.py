import email
from email.policy import default
from gettext import Catalog
from os import name
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "books.db"
# db = SQLAlchemy(app)





# Default DB (required even if you don’t use it)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///default.db"

# Your two extra databases
app.config['SQLALCHEMY_BINDS'] = {
    "books":  "sqlite:///books.db",
    "users":  "sqlite:///users.db",
    "branches": "sqlite:///branches.db",
    "catalog": "sqlite:///catalog.db"
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Book(db.Model):
    __bind_key__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    book_type = db.Column(db.String(25))
    lang = db.Column(db.String(15))
    quantity = db.Column(db.Integer)

class User(db.Model):
    __bind_key__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    username = db.Column(db.String(20))

class Branch(db.Model):
    __bind_key__ = "branches"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    contact_no = db.Column(db.Integer)
    location = db.Column(db.String(25))


class Catalog(db.Model):
    __bind_key__ = "catalog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    due_date = db.Column(db.DateTime)
    date_time = db.Column(db.DateTime, default = datetime.utcnow)




Model_Mapping = {
    "Book" : Book,
    "User" : User,
    "Branch": Branch,
    "Catalog": Catalog
}
Page_Mapping = {
    "Book" : "books",
    "User" : 'users',
    "Branch": "branches",
    "Catalog": "catalog"
}




@app.route("/", methods = ['GET', 'POST'])
def signin():
    return render_template('index.html')





@app.route("/dashboard", methods = ['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')



@app.route("/forgotpassword", methods = ['GET', 'POST'])
def forgotpswd():
    return render_template('forgotpswd.html')



@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template('signup.html')



@app.route("/admin_otp_form", methods = ['GET', 'POST'])
def admin_otp_form():
    return render_template('admin_otp_form.html')


@app.route("/reset_psswd", methods = ['GET', 'POST'])
def reset_psswd():
    return render_template('reset_psswd.html')


@app.route("/catalog", methods = ['GET', 'POST'])
def catalog():
    return render_template('Catalog.html')

@app.route("/books", methods = ['GET', 'POST'])
def books():
    allBooks = Book.query.all()
    return render_template('books.html', allBooks = allBooks)


@app.route("/users", methods = ['GET', 'POST'])
def users():
    allUsers = User.query.all()
    return render_template('users.html', allUsers = allUsers)
@app.route("/branches", methods = ['GET', 'POST'])
def branches():
    allBranches = Branch.query.all()

    return render_template('branches.html', allBranches = allBranches)




# Popups
@app.route("/add_book", methods = ['GET', 'POST'])
def add_book():
    if request.method == "POST":
        name = request.form['name']
        language = request.form['language']
        book_type = request.form['type']
        qty = request.form['quantity']
        newBook = Book(name = name,book_type = book_type,lang = language,quantity = qty)
        db.session.add(newBook)
        db.session.commit()
        return redirect('/books')
        
    return render_template('popups/add book.html', btn = "ADD")



@app.route("/add_user", methods = ['GET', 'POST'])
def add_user():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        newUser = User(name = name,email = email,username = username)
        db.session.add(newUser)
        db.session.commit()
        return redirect('/users')
    return render_template('popups/add user.html', btn = "ADD")

@app.route("/add_branch", methods = ['GET', 'POST'])
def add_branch():
    if request.method == "POST":
        name = request.form['name']
        contact_no = request.form['contact_no']
        location = request.form['location']
        newBranch = Branch(name = name,contact_no = contact_no,location = location)
        db.session.add(newBranch)
        db.session.commit()
        return redirect('/branches')
    return render_template('popups/add branch.html', btn = "ADD")




# Update

@app.route("/update_branch/<int:id>", methods = ['GET', 'POST'])
def update_branch(id):
    if request.method == "POST":
        name = request.form['name']
        contact_no = request.form['contact_no']
        location = request.form['location']
        branch = Branch.query.filter_by(id = id).first()
        branch.name = name
        branch.contact_no = contact_no
        branch.location = location
        db.session.add(branch)
        db.session.commit()
        return redirect('/branches')
    branch = Branch.query.filter_by(id=id).first()
    return render_template('popups/update branch.html', btn = "UPDATE", branch = branch)

@app.route("/update_user/<int:id>", methods = ['GET', 'POST'])
def update_user(id):
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        user = User.query.filter_by(id = id).first()
        user.name = name
        user.email = email
        user.username = username
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    user = User.query.filter_by(id=id).first()
    return render_template('popups/update user.html', btn = "UPDATE", user = user)

@app.route("/update_book/<int:id>", methods = ['GET', 'POST'])
def update_book(id):
    if request.method == "POST":
        name = request.form['name']
        language = request.form['language']
        book_type = request.form['book_type']
        quantity = request.form['quantity']
        book = Book.query.filter_by(id = id).first()
        book.name = name
        book.language = language
        book.book_type = book_type
        book.quantity = quantity
        db.session.add(book)
        db.session.commit()
        return redirect('/books')
    book = Book.query.filter_by(id=id).first()
    return render_template('popups/update book.html', btn = "UPDATE", book = book)


# Delete

@app.route("/delete/<int:id>/<string:dbms>", methods = ["GET", "POST"])
def delete(id,dbms):
    if request.method == "POST":
        model = Model_Mapping.get(dbms)
        page = Page_Mapping.get(dbms)
        to_del = model.query.filter_by(id=id).first()
        db.session.delete(to_del)
        db.session.commit()
        return redirect(f"/{page}")
    page = Page_Mapping.get(dbms)
    model = Model_Mapping.get(dbms)
    to_del = model.query.filter_by(id=id).first()
    return render_template('/popups/delete.html', dbms=dbms, to_del = to_del, page = page, btn = "CONFIRM")
        

# @app.route("/delete_user/<int:id>")
# def delete_user(id):
#     if request.method == "POST":
#         del_yes = request.form['del_yes']
#         if del_yes.lower() == "yes":
#             user = User.query.filter_by(id = id).first()
#             db.session.delete(user)
#             db.session.commit()
#             return redirect("/users")
        
#     user = User.query.filter_by(id = id).first()
#     return render_template('popups/delete user.html', btn = "CONFIRM", user = user)







if __name__ == "__main__":
    # with app.app_context():
    #     print("CREATING DATABASE NOW...")
    #     db.create_all()
    app.run(debug=True)
