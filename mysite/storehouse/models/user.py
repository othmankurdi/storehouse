import django
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.validators import RegexValidator
from django.db import models


class User(models.Model):
    auth_user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE,
                                  related_name='auth_user_id', null=True, blank=True)
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    age = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50)
    bio = models.TextField(max_length=200, blank=True)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.full_name
