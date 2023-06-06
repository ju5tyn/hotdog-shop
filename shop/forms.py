from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Regexp
from shop.models import User

class RegistrationForm(FlaskForm):
	username = StringField('user name',validators=[DataRequired(),Regexp('^[A-Za-z0-9]{5,20}$',message='Your username should be between 5 and 20 characters long.')])
	
	password = PasswordField('password',validators=[DataRequired(),Regexp('^[A-Za-z0-9]{5,20}$',message='Your password should be between 5 and 20 characters long.'),EqualTo('confirm_password', message='Passwords do not match. Try again')])
	confirm_password = PasswordField('confirm Password',validators=[DataRequired()])
	
	submit = SubmitField('register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Username already exists. Please choose a different one.')

class CheckoutForm(FlaskForm):
	name = StringField('full name',validators=[DataRequired(),Regexp('^[A-Za-z ]{1,50}$',message='Your name should be between 1 and 50 characters long')])
	
	card_no = StringField('card number',validators=[DataRequired(),Regexp('^\d{16}$',message='Your card number should be 16 digits long.')])
	
	submit = SubmitField('pay')
	
	
class ReviewForm(FlaskForm):
	subject = StringField('subject', validators=[DataRequired(),Regexp('^[A-Za-z ]{1,40}$',message='Subject can be maximum 40 characters')])
	description = StringField('description', validators=[DataRequired(),Regexp('^[A-Za-z ]{1,300}$',message='Description can be maximum 300 characters')])
	rating = StringField('rating', validators=[DataRequired(),Regexp('^[1-5]{1}$',message='Rating must be between 1 and 5')])
	
	submit = SubmitField('add review')


class LoginForm(FlaskForm):
	username = StringField('user name',validators=[DataRequired()])
	password = PasswordField('password',validators=[DataRequired()])
	submit = SubmitField('login')
	
	
class SortingForm(FlaskForm):
	sort_type = SelectField("sort by", choices=[("price_high", "High-Low"),
	("price_low", "Low-High"),("eco_low", "Eco friendly"), ("default", "Reccomended")], default="default",
	render_kw={"onchange": "this.form.submit()"})

class SearchForm(FlaskForm):
  	search = StringField('search', [DataRequired()])
  	submit = SubmitField('search', render_kw={'class': ''})