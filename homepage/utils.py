from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def confirmEmailAddress(emailAddress):
	try:
		validate_email(emailAddress)
		isValidEmail = True
	except ValidationError:
		isValidEmail = False
		return 'Invalid Email'


	# checking if email already exists
	if isValidEmail:
		if User.objects.filter(email=emailAddress).exists():
			return 'Email Already Exists'
		else:
			return 'Success'
	else:
		return 'Invalid Email'

def confirmUsername(username):
	if re.search("^(?=.{5,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$", username):
		if User.objects.filter(username=username).exists():
			return 'Username taken'
		else:
			return 'Success'
	else:
		return 'Invalid Username. Must contain alpa-numeric characters only, and between 5 to 20 characters long'

def confirmPassword(password):
	if len(password) > 20:
		return 'Password must be lesser than 20 characters long'
	elif len(password) < 5:
		return 'Password must be at least 5 characters long'
	else:
		return 'Success'