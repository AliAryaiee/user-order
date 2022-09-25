from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    """
        User Account Manger
    """

    def create_user(self, first_name, last_name, mobile, password=None):
        """
            Creates and Saves a User with the Given Firest Name, Last Name, Mobile and Password.
        """
        if not mobile:
            raise ValueError("Users Must Have an Valid Mobile Number!")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  first_name, last_name, mobile, password=None):
        """
            Creates and Saves a User with the Given Firest Name, Last Name, Mobile and Password.
        """
        user = self.create_user(
            first_name,
            last_name,
            mobile,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        User Account
    """
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    mobile = models.CharField(max_length=11, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.mobile
