from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from owners.models import SharedSite


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CurrentSiteUserManager(CurrentSiteManager, UserManager):
    pass


class User(SharedSite, AbstractUser):

    username = None  # unset username field from AbstractUser
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    objects = UserManager()
    current_site_objects = CurrentSiteUserManager()

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.email
