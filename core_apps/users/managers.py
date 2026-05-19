"""
User manager module.
"""
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Docstring for CustomUserManager
    """
    def _email_validator(self, email):
        """
        Validating email and raising related error.
        """
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))

    def create_user(self, first_name, last_name, email, password, **extra_fields):
        """
        Handling creation of User object.
        """
        if not first_name:
            raise ValueError(_("User must have a first name."))
        if not last_name:
            raise ValueError(_("User must have a last name."))
        if not password:
            raise ValueError(_("User must have a password."))
        if email:
            email = self.normalize_email(email)
            self._email_validator(email)
        else:
            raise ValueError(_("User must have email address."))

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        """
        Handling creation of superuser.
        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError(_("Superuser must have a password."))

        if email:
            email = self.normalize_email(email)
            self._email_validator(email)
        else:
            raise ValueError(_("Superuser must have an email."))

        user = self.create_user(first_name, last_name, email, password, **extra_fields)

        return user
