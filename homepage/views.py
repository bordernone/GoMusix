#homepage/views.py
from django.views.generic import TemplateView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .utils import confirmEmailAddress, confirmUsername, confirmPassword
import re

def homePageView(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('dashboard/')
	title = {'title':'GoMusix | Play your music everywhere'}
	return render(request, 'home.html', title)

def registerEmail(request):
	result = confirmEmailAddress(request.POST['email'])
	return HttpResponse(result)

def completeRegistration(request):
	username = request.POST['username']
	password = request.POST['password']
	email = request.POST['email']
	verifyEmail = confirmEmailAddress(email)
	verifyUsername = confirmUsername(username)
	verifyPassword = confirmPassword(password)

	if verifyEmail=='Success':
		if verifyUsername=='Success':
			if verifyPassword=='Success':
				query = User.objects.create_user(username=username, password=password, email=email)
				query.save()
				return HttpResponse('Registration Complete')
			else:
				return HttpResponse(verifyPassword)
		else:
			return HttpResponse(verifyUsername)
	else:
		return HttpResponse(verifyEmail)

def loginUser(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponse('Success')
	else:
		return HttpResponse('Incorrect username or password')

def logoutUser(request):
	logout(request)
	return redirect('/')