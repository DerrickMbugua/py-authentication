from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError, SubmitField
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# create the extension
db = SQLAlchemy()

app = Flask(__name__)
bcrypt = Bcrypt(app)
# configure the mysql database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mwema:%s@localhost/god_in_a_box'% quote('Mwema-1234')
#secret key
app.config['SECRET_KEY'] = "my long secret key veryy"
# initialize the app with the extension
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
  

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()

  
class RegistrationForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(),
        # validators.EqualTo('confirm', message='Passwords must match')
    ])
    submit = SubmitField('Register')
    # confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')
            
class LoginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(),
    ])
    submit = SubmitField('Login')


@app.route("/")
def hello_world():
    return render_template('home.html')
      
  
@app.route('/login', methods=['GET', 'POST'])
def login():
  # default_value = '0'
  # username = request.form.get('username', default_value)
  # app.logger.info(username)
  # password = request.form.get('password', default_value)
  # app.logger.info(password)
  app.logger.info("Start login")
  form = LoginForm(request.form)
  if request.method == 'POST' and form.validate():
     user = User.query.filter_by(username=form.username.data).first()
     if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
  return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
  
  
@app.route('/register', methods=['GET', 'POST'])
def register():
  app.logger.info("Start registration")
  form = RegistrationForm(request.form)
  if request.method == 'POST' and form.validate():
        app.logger.info("Mid registration")
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash('Thanks for registering')
        app.logger.info("End registration")
        return redirect(url_for('login'))
  return render_template('register.html', form=form)