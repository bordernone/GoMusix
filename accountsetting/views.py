from django.shortcuts import render
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from homepage.utils import confirmPassword

# Create your views here.
def accountSetting(request):
	if request.user.is_authenticated:
		title = {'title':'Change your account settings | GoMusix'}
		return render(request, 'accountsetting.html', title)
	else:
		if settings.DEBUG:
			return HttpResponse('You are not logged in')
		else:
			return Http404

def changePassword(request):
	if request.user.is_authenticated:
		if request.method != 'POST':
			if settings.DEBUG:
				return HttpResponse('Method must be POST')
			else:
				return Http404
		else:
			if 'newpassword' not in request.POST:
				return HttpResponse('No new password submitted')
				
			username = request.user.username
			newPassword = request.POST['newpassword']
			isPasswordValid = confirmPassword(newPassword)
			if isPasswordValid == 'Success':
				currentUser = User.objects.get(username__exact=username)
				currentUser.set_password(newPassword)
				currentUser.save()
				return HttpResponse('success')
			else:
				return HttpResponse(isPasswordValid)

	else:
		if settings.DEBUG:
			return HttpResponse('You are not logged in')
		else:
			return Http404