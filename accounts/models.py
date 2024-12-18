from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)  # Ensure is_staff is set for superuser
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        max_length=255,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=150)
    phone = models.BigIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Add this field
    is_superuser = models.BooleanField(default=False)  # Optionally add this field
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
