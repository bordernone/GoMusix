# accountsetting/urls.py
from django.urls import path, re_path
from .views import accountSetting, changePassword

urlpatterns = [
    path('settings/', accountSetting, name='accountsetting'),
    path('settings/changepassword/', changePassword, name='changePassword'),
]