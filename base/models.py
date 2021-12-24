from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from base.managers import CustomUserManager


class Website(models.Model):
    site_name = models.CharField(max_length=100)
    website_url = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to='website/logo/', default='website/logo/default.png',
        help_text='Resolution: 108x21'
    )
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    short_desc = models.TextField(max_length=500, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    youtube = models.CharField(max_length=100, blank=True)
    otp_api_key = models.CharField(max_length=200, blank=True)
    payment_api_key = models.CharField(max_length=200, blank=True)
    google_api_key = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.site_name


class CustomUser(AbstractUser):
    CREATOR = _('Creator')
    SUBSCRIBER = _('SUBSCRIBER')

    ROLE_CHOICES = (
        (CREATOR, 'Creator'),
        (SUBSCRIBER, 'Subscriber')
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    profile_picture = models.ImageField(default='user/images/fce502bf-2e2a-49b2-bcda-e4bfb4ef7c02.jpeg', null=True,
                                        upload_to='user/images/')

    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def image_preview(self):
        if self.profile_picture:
            return mark_safe(f'<img src="{self.profile_picture.url}" width="100" height="60">')

    @property
    def image_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url'):
            return self.profile_picture.url


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='user/images')
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.email
