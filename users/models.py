from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin


class User(AbstractUser, PermissionsMixin):
    pass
