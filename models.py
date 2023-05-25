from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dateutil.relativedelta import relativedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = '229b845d2e364ca8a032e35c104f69b1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='vrslightmodecoders@gmail.com',
    MAIL_PASSWORD='mamfyuvcggdfhewh',
)
mail=Mail(app)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mobileNo = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable= False)
    password = db.Column(db.String(50),nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, name, mobileNo, email, password):
        self.name=name
        self.mobileNo=mobileNo
        self.email=email
        self.password=password
        self.status=1


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobileNo = db.Column(db.String(120), unique=True, nullable=False)
    agentID = db.Column(db.Integer, nullable=False)
    
    collection = db.Column(db.Integer, nullable=False)
    closingBalance = db.Column(db.Integer, nullable=False)

    def __init__(self, name, mobileNo, agentID, collection=0, closingBalance=0):
        self.name = name
        self.mobileNo = mobileNo
        self.collection = collection
        self.closingBalance = closingBalance
        self.agentID = agentID

with app.app_context():
    db.create_all()
