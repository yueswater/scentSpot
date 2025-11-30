from django.db import models
from django.contrib.auth.models import User as AuthUser


class User(models.Model):
    """Staff user for perfume usage tracking"""
    name = models.CharField(max_length=100)
    auth_user = models.OneToOneField(
        AuthUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_profile'
    )

    def __str__(self):
        return self.name


class Perfume(models.Model):
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    capacity_ml = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} - {self.name} ({self.capacity_ml}ml)"


class UsageLog(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Unspecified", "Unspecified"),
    ]

    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, default="Unspecified")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='logs'
    )
    perfume = models.ForeignKey(
        Perfume, on_delete=models.CASCADE, related_name='logs'
    )
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.gender}] {self.perfume.name} at {self.used_at}"
