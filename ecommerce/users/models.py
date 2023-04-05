import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for E-Commerce.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def __str__(self):
        """
        Get the string representation of the user.
        """
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE,
    )

    full_name = models.CharField(blank=True, max_length=255)
    birth_date = models.DateField(blank=True)
    avatar = models.ImageField(blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(blank=True, max_length=255)
    contact_email = models.EmailField(blank=True)
    country = models.CharField(blank=True, max_length=255)
    language = models.CharField(blank=True, max_length=255)
    allow_email_contact = models.BooleanField()
    allow_phone_contact = models.BooleanField()
    allow_marketing = models.BooleanField()

    def __str__(self):
        return f"{ self.user.email }"
