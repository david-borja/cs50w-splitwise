from django.db import models
from django.utils import timezone
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


class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    group = models.ForeignKey(
        UserGroup, blank=True, null=True, on_delete=models.CASCADE, related_name="group_expenses"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(
        UserAlias,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="acquisitions",
    )
    currency = models.CharField(
        max_length=3, choices=[("EUR", "Euro"), ("USD", "Us Dollar")], blank=False, null=False, default="EUR"
    )
    splitters = models.ManyToManyField(UserAlias, related_name="shared_expenses")
    icon = models.CharField(max_length=64, default="💳")
    timestamp = models.DateTimeField(default=timezone.now)
