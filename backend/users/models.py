from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import pyotp
import sys

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, login_intra=None, display_name=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        if password is None:
            raise ValueError("User must have a password")
        user = self.model(email=self.normalize_email(email), username=username, display_name=username, login_intra=login_intra)
        user.set_password(password)
        # check password is hashed or not
        # print(user.password, file=sys.stderr)
        user.save(using=self._db)
        user.secret_2FA = pyotp.random_base32()
        return user
    
    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

def profile_image(instance):
    return f'/static/users/profile_images/{instance.id}/'

def default_profile_image():
    return '/static/users/profile_images/default.jpg'

# Create your models here.
class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username        = models.CharField(max_length=32, unique=True)
    display_name    = models.CharField(max_length=32, unique=False)
    login_intra     = models.CharField(max_length=32, unique=True, null=True, blank=True)
    profile_image   = models.ImageField(max_length=255, upload_to=profile_image, null=True, blank=True, default=default_profile_image)

    # 2FA fields
    enabled_2FA     = models.BooleanField(default=False)
    secret_2FA      = models.CharField(max_length=16, unique=True, null=True, blank=True)
    waiting_2FA     = models.DateTimeField(null=True, blank=True)
    nb_try_2FA      = models.IntegerField(default=0)

    # Required fields for admin panel work properly
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    # This is what it returns when you don't access to a specific field
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def get_authentification_setup_uri(self):
        return pyotp.totp.TOTP(self.secret_2FA).provisioning_uri(self.username, issuer_name="Transcendence")
    
    def is_otp_valid(self, otp):
        return pyotp.TOTP(self.secret_2FA).verify(otp)
