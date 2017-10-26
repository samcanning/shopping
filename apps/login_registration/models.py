# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re
import bcrypt

class UserMgr(models.Manager):
    def regvalidator(self, postData):
        errors = {}
        emailRegex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" #email format
        nameRegex = r"(^[a-zA-Z]+$)" #letters only
        pwRegex = r"(^[a-zA-Z0-9_.!?-]+$)" #valid password characters (alphanumeric characters or _.!?-)

        #name
        if not re.match(nameRegex, postData['fname']):
            errors['fname'] = "Must enter a valid first name."
        else:
            if len(postData['fname']) < 2:
                errors['fname'] = "First name must be at least 2 characters."
            elif len(postData['fname']) > 255:
                errors['fname'] = "First name cannot be longer than 255 characters."
        if not re.match(nameRegex, postData['lname']):
            errors['lname'] = "Must enter a valid last name."
        else:
            if len(postData['lname']) < 2:
                errors['lname'] = "Last name must be at least 2 characters."
            elif len(postData['lname']) > 255:
                errors['lname'] = "Last name cannot be longer than 255 characters." 
        #email
        if not re.match(emailRegex, postData['email']):
            errors['email'] = "Must be a valid email address."
        elif User.objects.filter(email=postData['email']).exists():
            errors['email'] = "This email address is already in use."
        #password
        if str.lower(str(postData['password'])) == 'password':
            errors['password'] = "Password cannot be 'password'."
        elif not re.match(pwRegex, postData['password']):
            errors['password'] = "Not a valid password."
        else:
            if len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters."
            elif postData['password'] != postData['confirmpw']:
                errors['password'] = "Passwords must match."
        return errors

    def loginvalidator(self, postData):
        errors = {}

        try:
            this = User.objects.get(email=postData['email'])
        except:
            errors['email'] = "No user found with this email address."
        
        if 'email' not in errors:
            pw_attempt = str(postData['password'])
            pw_to_check = str(this.password)
            if not bcrypt.checkpw(pw_attempt, pw_to_check):
                errors['password'] = "Incorrect password."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserMgr()