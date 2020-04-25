from flask import Flask, redirect, url_for, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, RadioField, validators, DecimalField, FloatField
from wtforms.validators import input_required, DataRequired
import pandas as pd
import numpy as np
import joblib
from flask_bootstrap import Bootstrap
from loginform import Loginf, Reginf
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin, login_user, current_user, logout_user, login_required





app = Flask(__name__)


app.config['SECRET_KEY'] = '65638HtY8818'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class UserForm(FlaskForm):
    age = IntegerField('Age', validators = [input_required()])
    gender = RadioField(u'Gender', choices=[(1, 'Male'),(0, 'Female')], validators = [input_required(), DataRequired()])
    restBP = IntegerField('Resting BP', validators = [input_required(), DataRequired()])
    chestPain = SelectField(u'ChestPain', choices=[(0, 'Typical Agina'), (1, 'Atypical Agina'), (2, 'Non Agina'), (3 ,'Asymptotic')], validators = [input_required(), DataRequired()])
    cholestrol = IntegerField('Cholestrol', validators=[input_required()])
    bloodSugar = RadioField(u'BloodSugar', choices=[(0, 'Yes'), (1, 'No')], validators = [input_required(), DataRequired()])
    restEcg = SelectField('RestECG', choices=[(0, 'normal'), (1, 'ST-T Wave Abnormality'), (2, 'Left Ventricular Hypertropy')], validators = [input_required(), DataRequired()])
    maxHeart = IntegerField('Max. Heart rate', validators = [input_required()])
    exang = RadioField('Exercise Indiced Agina', choices=[(1, 'Yes'), (0, 'No')], validators = [input_required(), DataRequired()])
    oldPeak = FloatField('ST depression', validators = [input_required(), DataRequired()])
    slope = SelectField('Slope', choices=[(0, 'Up Sloping'), (1, 'Down Sloping'), (2, 'flat')], validators = [input_required(), DataRequired()])
    thal = SelectField('Thalassemia', choices = [(0, 'No'), (1, 'Normal'), (2, 'Fixed Defect'), (3, 'Irreversible')], validators = [input_required(), DataRequired()])



@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/register", methods = ['POST', 'GET'])
def register():
    form = Reginf()
    if form.validate_on_submit():
        newUser = User(username = form.uname.data, email = form.email.data, password = form.pwd.data)
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('login'))
        #return '<h1>' + form.uname.data + ' ' + form.email.data + '</h1>'

    return render_template("registration.html", form=form)

@app.route("/")
@app.route("/login", methods = ['POST', 'GET'])
def login():
    form = Loginf()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.uname.data).first()
        if user and form.pwd.data == user.password :
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')

    return render_template("login.html", form = form, name = "login")



@app.route("/predict", methods = ['POST', 'GET'])
@login_required
def predict():
    form = UserForm()
    if form.validate_on_submit() or request.method == 'POST':
        mydict = form.data
        df = pd.DataFrame(mydict, index = [0])
        df = df.drop(['csrf_token'], axis = 1)
        ohe = ['chestPain', 'restEcg', 'slope', 'thal', 'gender']
        ohe_col=joblib.load("C:\\Users\\KurellaYash\\Desktop\\EHDP\\allcol.pkl")
        df_processed = pd.get_dummies(df, columns=ohe)
        newdict={}
        for i in ohe_col:
            if i in df_processed.columns:
                newdict[i]=df_processed[i].values
            else:
                newdict[i]=0

        newdf=pd.DataFrame(newdict)
        model = joblib.load("C:\\Users\\KurellaYash\\Desktop\\EHDP\\finalmodel.pkl")
        pred = model.predict(newdf)
        pred = pred > 0.54
        resdf=pd.DataFrame(pred, columns=['Status'])
        val = resdf.at[0, 'Status']


        return render_template("result.html", form = form, val = val, name = "Result")

    return render_template("predictform.html", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/admin")
def admin():
    n = current_user.username
    if(n == "admin"):
        user = User.query.all()
        return render_template("admin.html", user = user)
    else:
        return render_template("home.html")

   
if __name__ == "__main__":
    app.run(debug = True)
