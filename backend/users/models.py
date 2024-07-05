import io
import sys
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import pyotp, qrcode, os


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
        user.save(using=self._db)
        
        # Generate QR Code
        user.secret_2FA = pyotp.random_base32()
        qr = qrcode.make(user.get_authentification_setup_uri())
        buffer = io.BytesIO()
        qr.save(buffer, format='PNG')
        user.qrcode_2FA.save('qrcode.png', buffer, save=False)
        buffer.close()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

def profile_image(instance, filename):
    extension = filename.split('.')[-1]
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')

    return f'profile_images/{instance.id}_{timestamp}.{extension}'

def user_qrcode(instance, filename):
    return f'qrcodes/{instance.id}.png'

# Create your models here.
class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username        = models.CharField(max_length=32, unique=True)
    display_name    = models.CharField(max_length=32, unique=False)
    login_intra     = models.CharField(max_length=32, unique=True, null=True, blank=True)
    profile_image   = models.ImageField(max_length=255, upload_to=profile_image, null=True, blank=True)

    # user status
    is_online       = models.BooleanField(default=False)
    connection_count = models.IntegerField(default=0)

    # 2FA fields
    enabled_2FA     = models.BooleanField(default=False)
    secret_2FA      = models.CharField(max_length=32, unique=True, null=True, blank=True)
    qrcode_2FA      = models.ImageField(max_length=255, upload_to=user_qrcode, null=True, blank=True)
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
        return f"{self.username} <Account>"
    
    def save(self, *args, **kwargs):

        # If the user exists in the database
        if self.pk:
            old_user = Account.objects.get(pk=self.pk)

            # Delete old profile image
            if old_user.profile_image and old_user.profile_image != self.profile_image:
                old_user.profile_image.delete(save=False)

        super(Account, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_authentification_setup_uri(self):
        return pyotp.totp.TOTP(self.secret_2FA).provisioning_uri(self.username, issuer_name="Transcendence")

    def is_otp_valid(self, otp):
        return pyotp.TOTP(self.secret_2FA).verify(otp)

    def set_2FA(self, val: bool):
        self.enabled_2FA = val
        self.save()

    def set_date_2FA(self):
        if self.waiting_2FA is not None:
            self.waiting_2FA = None
        else:
            self.waiting_2FA = timezone.now()
        self.save()

    def compare_date_2FA(self):
        return (timezone.now() - self.waiting_2FA).seconds > 60
    
    def get_profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return '/static/images/default_profile_image.jpg'