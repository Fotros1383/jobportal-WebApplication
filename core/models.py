from django.db import models
from django.contrib.auth.models import AbstractUser

class SiteUser(AbstractUser):
    ROLE_CHOICES = [
        ('EMPLOYER', 'Employer'),
        ('JOB_SEEKER', 'Job seeker')
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Resume(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


