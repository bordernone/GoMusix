from django.db import models

# Create your models here.
class UserSong(models.Model):
	sn = models.IntegerField(primary_key=True)
	username = models.CharField(max_length=100)
	mimetype = models.CharField(max_length=50)
	originalname = models.CharField(max_length=100)
	timesplayed = models.IntegerField(default=0)