from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
  pass

class UserAlias(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  alias = models.CharField(max_length=64)
  group = models.ForeignKey("UserGroup", blank=False, null=False, on_delete=models.CASCADE, related_name="participants")
  user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="aliases")


class UserGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True, null=True)
    icon = models.CharField(max_length=64, default="💸")
