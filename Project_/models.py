from django.db import models #type: ignore


from django.db import models

class DTP(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=255)
    name_dri1 = models.CharField(max_length=255)
    name_dri2 = models.CharField(max_length=255)
    license_plate1 = models.CharField(max_length=20, null=True)
    license_plate2 = models.CharField(max_length=20, null=True)
    insurance = models.CharField(max_length=255)
    image = models.ImageField(upload_to='dtp_drawings/', null=True, blank=True)  # Додаємо поле для малюнка

    def __str__(self):
        return f'{self.date} - {self.location}'

# Create your models here.
