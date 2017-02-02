from __future__ import unicode_literals
from django.db import models
import bcrypt, re

# Email name regex patterns

REGEX_EMAIL=r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$'
#instructions say letters only Modified
# - allows a dash, \s allows a space,  \' allows apostrophe
# Realistically, check only for minimum and maximum characters
REGEX_NAME= r'^([a-zA-Z]*)([-\s\'][a-zA-Z]*)*$'
# regex_name= r'^[a-zA-Z]*$'

class UserManager(models.Manager):
    def register (self, data):
        print "in UserManager register"
        errors = []
        first_name = data['firstname']
        last_name = data['lastname']
        email = data['email'] #register email
        password = data['password']
        confirm_pw = data['confirm_pw']

        if len(first_name) < 3:
            errors.append("Please enter your first name.")
        elif not re.match(REGEX_NAME,first_name):
            errors.append("Please enter only letters in your first name.")

        if len(last_name) < 3:
            errors.append("Please enter your last name.")
        elif not re.match(REGEX_NAME,last_name):
            errors.append("Please enter only letters in your last name.")

        if len(email) == 0:
            errors.append("Please enter your email address.")
        elif not re.match(REGEX_EMAIL,email):
            errors.append("Please enter a valid email address.")
        else: # duplicate_email_check
            if User.objects.filter(email=email).exists():
                errors.append("That email address already exists in the database. Please enter a different email address.")

        if len(password) < 8:
            errors.append("Your password must be at least 8 characters long.")
        elif password != confirm_pw:
            errors.append("Your passwords don't match.")
        else:
            pw = password.encode()
            hashpassword = bcrypt.hashpw(pw,bcrypt.gensalt())
        if errors:
            print errors
            return(False, errors)
        else: #No errors. Write user to database
            action =self.create(first_name=first_name,last_name=last_name,email=email,password=hashpassword)
            action.save()
            errors = []
            return (True, errors)

    def login (self, data):
        # check for email first
        email = data['loginemail']
        password = data['password']
        if User.objects.filter(email=email).exists(): # email is in database
            user = User.objects.get(email=email) # Get user object
            userpw = user.password.encode() # stored password for user
            provided_pw = password.encode()
            if bcrypt.hashpw(provided_pw, userpw) == userpw:
                print "passwords match"
                return (True)
            else:
                return (False)
        else: # email doesn't exist
            return (False)

    def deleteuser (self, id):
        action = self.get(id=id)
        action.delete()

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    # birthdate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # Connect UserManager to User class to add methods
    objects = UserManager()
