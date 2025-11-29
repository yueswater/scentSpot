from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)

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
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unspecified'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='logs')
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_gender_display()}] {self.perfume.name} at {self.used_at}"
