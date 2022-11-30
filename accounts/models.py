from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        validators=[MinLengthValidator(5)], max_length=16, unique=True
    )
    last_name = models.CharField(validators=[MinLengthValidator(1)], max_length=20)
    first_name = models.CharField(validators=[MinLengthValidator(1)], max_length=20)
    address = models.CharField(max_length=50)

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"
