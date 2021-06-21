from django.contrib import messages
from django.contrib.messages.api import error
from django.db import models
import re
from datetime import datetime, timedelta

from django.shortcuts import redirect
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        NAME_REGEX= re.compile(r'^[a-zA-z]+$')
        if len(post_data['first_name']) < 2 or not NAME_REGEX.match(post_data['first_name']):
            errors['firstname']= "First name must be at least 2 characters long and only letters."
        if len(post_data['last_name']) < 2 or not NAME_REGEX.match(post_data['last_name']):
            errors['lastname']= "Last name must be at least 2 characters long, only letters."
        if len(post_data['birthday']) == 0:
            errors['bd']= "Birthday must be mm/dd/yyy."
        if len(post_data['birthday']) != 0:
            if datetime.strptime(post_data['birthday'], "%Y-%m-%d")> datetime.today():
                errors['bd_input']= "Birthday can't be in the future."
            user_bd= datetime.strptime(post_data['birthday'], "%Y-%m-%d")
            x= datetime.now() - timedelta(weeks=52*13)
            if user_bd > x and user_bd < datetime.now():
                errors['bday_input']= "Users under 13 can't register."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address."
        check_email= User.objects.filter(email= post_data['email'])
        if check_email:
            errors['email_input']= "This email address already exists."
        if len(post_data['password']) < 8:
            errors['password']= "Password must be at least 8 characters long."
        if post_data['confirm_pw'] != post_data['password']:
            errors['confirm_pw']= "Passwords don't match."
        return errors

    def login_validator(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['log_email'] = "Invalid email address."
            return errors
        if len(post_data['password']) < 8:
            errors['password']= "Password must be at least 8 characters long."
        user= User.objects.filter(email=post_data['email'])
        if user:
            user= user[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors['log_password']= "Incorrect password."
        else:
            errors['log_email_password']= "Incorrect email."
        return errors

    def update_validator(self, post_data, user):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not bcrypt.checkpw(post_data['curr_password'].encode(), user.password.encode()):
            errors['curr_password']= "Password does not match, Can't update profile."
            return errors
        if post_data['first_name'] != "":    
            if len(post_data['first_name']) < 2 or len(post_data['first_name'])> 50:
                errors['firstname']= "First name must be between 2 and 50 characters long"
        if post_data['last_name'] != "": 
            if len(post_data['last_name']) < 2 or len(post_data['last_name'])> 50:
                errors['lastname']= "Last name must be between 2 and 50 characters long"
        if post_data['email'] != user.email and post_data['email'] != "":
            check_email= User.objects.filter(email= post_data['email'])
            if check_email:
                errors['email_input']= "This email address already in use"
            if not EMAIL_REGEX.match(post_data['email']):
                errors['email'] = "Invalid email address"
        if post_data['new_password'] != "":
            if len(post_data['new_password']) < 8:
                errors['new_password']= "New password must be at least 8 characters long"
            if post_data['new_password'] != post_data['new_confirm_pw']:
                errors['new_ confirm_pw']= "Passwords do not match."
        return errors


class User(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    birthday= models.DateTimeField()
    email= models.CharField(max_length=100, unique=True)
    password= models.CharField(max_length=60)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()
