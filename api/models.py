from django.db import models

# Create your models here.
class apiKeys(models.Model):
    username = models.CharField(max_length=100)
    apiToken = models.CharField(max_length=100)
    apiRefreshToken = models.CharField(max_length=100)

    def __str__(self):
        return self.username