from flask import Flask
#import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "62b2a4f8fcdcd2b8a449d40213aa15894bfcba16d14305b4"

# suppress SQLAlchemy warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# config that allows us to access the mySQL database
#basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21063740:Mynamejeff123@csmysql.cs.cf.ac.uk:3306/c21063740_hotdog_db'
#app.run(host="localhost", port=5000)

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
