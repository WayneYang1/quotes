# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import User, Quote

# Create your views here.
def index(request):
	return render(request, 'quotes_app/index.html')

def register(request):
	post_data = request.POST.copy()
	result = User.objects.register(post_data)
	if isinstance(result, list):
		for err in result:
			messages.error(request, err)
		return redirect(reverse('quotes:index'))
	else:
		request.session['user'] = result
		return redirect(reverse('quotes:quotes'))

def login(request):
	post_data = request.POST.copy()
	result = User.objects.login(post_data)
	if isinstance(result,list):
		for err in result:
			messages.error(request, err)
		return redirect('/')
	else:
		request.session['user'] = result
		return redirect(reverse('quotes:quotes'))

def quotes(request):
	if 'user' not in request.session:
		return redirect('/')
	else:
		user = User.objects.get(id=request.session['user'])
		favorite_quotes = Quote.objects.filter(favorite=user)
		other_quotes = Quote.objects.exclude(id__in=favorite_quotes)
		context = {
			"user" : user,
			"favorite_quotes" : favorite_quotes,
			"other_quotes" : other_quotes
		}
		return render(request, 'quotes_app/quotes.html', context)

def user(request, user_id):
	if 'user' not in request.session:
		return redirect('/')
	user = User.objects.get(id=user_id)
	quotes = Quote.objects.filter(creator=user)
	context = {
		"user" : user,
		"quotes" : quotes
	}
	return render(request, 'quotes_app/users.html', context)

def favorite(request, quote_id):
	user = User.objects.get(id=request.session['user'])
	quote = Quote.objects.get(id=quote_id)
	user.favorited_quotes.add(quote)
	return redirect(reverse('quotes:quotes'))

def unfavorite(request, quote_id):
	user = User.objects.get(id=request.session['user'])
	quote = Quote.objects.get(id=quote_id)
	user.favorited_quotes.remove(quote)
	return redirect(reverse('quotes:quotes'))

def add(request):
	post_data = request.POST.copy()
	result = Quote.objects.validate_quote(post_data, request.session['user'])
	if isinstance(result, list):
		for err in result:
			messages.error(request, err)
		return redirect(reverse('quotes:quotes'))
	else:
		user = User.objects.get(id=request.session['user'])
		added_quote = Quote.objects.create(creator=user, quoted_by=request.POST['quoted_by'], content=request.POST['content'])
		return redirect(reverse('quotes:quotes'))

def logout(request):
	request.session.pop('user')
	return redirect('/')