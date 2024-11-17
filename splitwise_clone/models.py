from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
  pass

class UserGroup(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=256)
  description = models.CharField(max_length=256)
  icon = models.CharField(max_length=64)
  participants = models.ManyToManyField(User, related_name="own_groups")