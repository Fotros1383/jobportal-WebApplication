from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_EMPLOYER = 'E'
    ROLE_JOBSEEKER = 'J'
    MAX_LENGTH = 1
    ROLE_CHOICES = [
        (ROLE_EMPLOYER, 'Employer'),
        (ROLE_JOBSEEKER, 'job seeker')
    ]
    role = models.CharField(max_length=MAX_LENGTH, choices=ROLE_CHOICES)


class Resume(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resume/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


