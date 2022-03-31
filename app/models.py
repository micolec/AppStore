# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_buyer = models.BooleanField('Is buyer', default = False)
    is_seller = models.BooleanField('Is seller', default = False)
    is_superuser = models.BooleanField()
    username = models.CharField(primary_key=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'