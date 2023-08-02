from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Tworzy i zapisuje użytkownika z podanym adresem e-mail, datą
        urodzenia i hasłem.
        """
        if not email:
            raise ValueError('Użytkownicy muszą posiadać adres e-mail')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True,)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    objects = MyUserManager()

    USERNAME_FIELD = 'email'


