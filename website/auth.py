from flask import Blueprint , render_template , request , flash ,url_for , redirect
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth =Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))





@auth.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        month = request.form.get('month')
        income = request.form.get('income')
        expense = request.form.get('expense')
        if len(income) < 1:
                flash('Enter Income / Expense', category='error')
        elif len(expense) < 1:
            flash('Enter Income / Expense', category='error')
        else:
            new_note = Note(month = month,income=income, expense=expense, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Information added Successfully!', category='success')
            return redirect(url_for('auth.month'))
            note = Note.query.filter_by(month=month).first()
            if month==note.month:
                    a_user = db.session.query(Note).filter(Note.month == month).one()
                    a_user.income=income
                    a_user.expense=expense
                    db.session.commit()
                    flash("Data Updated Successfully!" , category="success")
                    return redirect(url_for('auth.home'))
       
    return render_template("home.html", user=current_user)



@auth.route("/signup", methods=['GET', 'POST'])

def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Oops! User alreday Exists , Use alternate Email Id', category='error')
        else:
            if len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash('Passwords dosen\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('auth.home'))
            
    return render_template("signup.html", user=current_user)


@auth.route('/update',methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1!=password2:
            flash("Confirm Password not match with new password", category="error")
            return redirect(url_for('auth.update'))
        elif len(password1 or password2) < 4:
            flash("Enter Strong Password", category="error")
            return redirect(url_for('auth.update'))

        user = User.query.filter_by(email=email).first()
        if user:
            a_user = db.session.query(User).filter(User.email == email).one()
            a_user.password=generate_password_hash(password1, method='sha256')
            db.session.commit()
            flash("Password Updated Successfully!" , category="success")
            return redirect(url_for('auth.home'))
                
            
    return render_template("update.html", user=current_user)
    



@auth.route('/month', methods=['GET', 'POST'])
def month():
    if request.method == 'POST':
        month = request.form.get('month')
        income = request.form.get('income')
        expense = request.form.get('expense')
        
        note = Note.query.filter_by(month=month).first()
        
        if month==note.month:
                a_user = db.session.query(Note).filter(Note.month == month).one()
                a_user.income=income
                a_user.expense=expense
                db.session.commit()
                flash("Data Updated Successfully!" , category="success")
                return redirect(url_for('auth.home'))
       
    return render_template("month.html", user=current_user)


