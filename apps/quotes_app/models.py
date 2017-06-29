# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
import datetime
from django.db import models

# Create your models here.
class UserManager(models.Manager):
	def register(self, data):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = []
		for field in data:
			if len(data[field]) == 0:
				errors.append(field.replace('_', ' ').title() + " may not be empty")
		if len(data['first_name']) < 2 or len(data['last_name']) < 2:
			errors.append("First Name and Last Name must be at least 2 characters long")
		if not data['first_name'].isalpha() or not data['last_name'].isalpha():
			errors.append("First Name and Last Name may only be letters")
		if not EMAIL_REGEX.match(data['email']):
			errors.append("Email not valid")
		if len(data['password']) < 8:
			errors.append("Password must be at least 8 characters long")
		if data['password'] != data['confirm_password']:
			errors.append("Passwords do not match")
		try:
			User.objects.get(email=data['email'])
			errors.append("Email already registered")
		except:
			pass
		try:
			birthday = datetime.datetime.strptime(data['birthday'], '%Y-%m-%d')
			today = datetime.datetime.today()
			if birthday > today:
				errors.append("Birthday must be before today")
		except:
			pass		
		if len(errors) == 0:
			hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
			user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], alias=data['alias'], email=data['email'], password=hashed_pw, birthday=data['birthday'])
			return user.id
		return errors

	def login(self, data):
		errors=[]
		for field in data:
			if len(data[field]) == 0:
				errors.append(field.replace('_', ' ').title() + " may not be empty")
		try:
			user = User.objects.get(email=data['email'])
			if bcrypt.hashpw(data['password'].encode(), user.password.encode()) == user.password.encode():
				return user.id
			else:
				errors.append("Incorrect password")
		except:
			errors.append("You have not registered your email")

		if len(errors) > 0:
			return errors


class QuoteManager(models.Manager):
	def validate_quote(self, data, user_id):
		errors=[]
		for field in data:
			if len(data[field]) == 0:
				errors.append(field.replace('_', ' ').title() + " may not be empty")
		if len(data['quoted_by']) < 4:
			errors.append('Quoted By field should be more than 3 characters long')
		if len(data['content']) < 11:
			errors.append('Quote should be more than 10 characters long')
		if len(errors) == 0:
			user = User.objects.get(id=user_id)
			created_quote = Quote.objects.create(creator=user, quoted_by=data['quoted_by'], content=data['content'])
			return created_quote
		return errors
		#quoted_by more than 3 characters
		#message more than 10 characters

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password= models.CharField(max_length=255)
	birthday = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Quote(models.Model):
	creator = models.ForeignKey(User, related_name='created_quote')
	favorite = models.ManyToManyField(User, related_name='favorited_quotes')
	quoted_by = models.CharField(max_length=255)
	content = models.CharField(max_length=255)
	objects = QuoteManager()
