from django.db import models
from django.contrib.auth.models import User
from Edum.settings import TOKEN_LENGTH

# Create your models here.
class ConfirmationToken(models.Model):
    user = models.OneToOneField(User, related_name="user_token")

    token = models.CharField(max_length=TOKEN_LENGTH)
    expiry_date = models.DateField()

