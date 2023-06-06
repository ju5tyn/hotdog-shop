from shop import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Item(db.Model):
	# Setup for fields in table
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, nullable=False)
	price = db.Column(db.Float, nullable=False)
	description = db.Column(db.Text, nullable=False)
	image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
	vegetarian = db.Column(db.Boolean, nullable=False)
	eco_rating = db.Column(db.Integer, nullable=False)
	calories = db.Column(db.Integer, nullable=False)
	
	# Printable representation of object
	def __repr__(self):
		return f"Post('{self.name}', '{self.price}', '{self.id}')"
		
		
class CartItem(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	session_id = db.Column(db.Integer, db.ForeignKey('cart_session.id'))
	item_id = db.Column(db.Integer, nullable=False)
	quantity = db.Column(db.Integer, nullable=False)
	
	
class CartSession(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	total = db.Column(db.Integer)
	items = db.relationship("CartItem", backref='cart_session', lazy=True)
	

class ItemReview(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	item_id = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	subject = db.Column(db.String(40), nullable=False)
	description = db.Column(db.String(300), nullable=False)
	rating = db.Column(db.Integer, nullable=False)
	
		


class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	hashed_password=db.Column(db.String(128))
	authenticated=db.Column(db.Boolean, default=False, nullable=False)
	carts=db.relationship("CartSession", backref='user', lazy=True)
	
	
	def __repr__(self):
		return f"User('{self.username}')"
	
	@property
	def password(self):
		raise AttributeError('Password is not readable.')
	
	@password.setter
	def password(self,password):
		self.hashed_password=generate_password_hash(password)
	
	def verify_password(self,password):
		return check_password_hash(self.hashed_password,password)
		
		
	def is_active(self):
		return True
	
	def get_id(self):
		return self.id
	
	def is_authenticated(self):
		return self.authenticated
	
	def is_anonymous(self):
		return False


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
