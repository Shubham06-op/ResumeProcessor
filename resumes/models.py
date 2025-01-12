from django.db import models

class Candidate(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} - {self.email}"
