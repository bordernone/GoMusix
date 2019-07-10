# homepage/urls.py
from django.urls import path

from .views import homePageView, registerEmail, completeRegistration, loginUser, logoutUser, recoverAccount

urlpatterns = [
    path('', homePageView, name='home'),
    path('register/email/', registerEmail, name='verifyEmail'),
    path('register/', completeRegistration, name='registration'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('recover/', recoverAccount, name='recover')
]