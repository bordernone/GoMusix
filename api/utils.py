from .models import apiKeys

def verifyToken(username, token):
    query = apiKeys.objects.all().filter(username=username, apiToken=token)
    if query.count() == 1:
        return True
    else:
        return False