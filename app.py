from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

# create the extension
db = SQLAlchemy()

app = Flask(__name__)

# configure the mysql database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mwema:%s@localhost/god_in_a_box'% quote('Mwema-1234')
#secret key
app.config['Secret_key'] = "my long secret key veryy"
# initialize the app with the extension
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return render_template('home.html')
  
  
@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/register')
def register():
  return render_template('register.html')