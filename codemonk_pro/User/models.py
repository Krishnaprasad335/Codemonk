from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, date_of_birth, password=None, **extra):
        if not email:
            raise ValueError("Email required.")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            date_of_birth=date_of_birth,
            **extra,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, name, date_of_birth, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, name, date_of_birth, password, **extra)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'date_of_birth']

