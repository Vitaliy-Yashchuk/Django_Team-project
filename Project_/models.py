from django.db import models #type: ignore


class DTP(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=255)
    name_dri1 = models.CharField(max_length=255)
    name_dri2 = models.CharField(max_length=255)
    license_plate = models.IntegerField()
    insurance = models.CharField(max_length=255)

    def __str__(self):
        return self.name_dri1

# Create your models here.
