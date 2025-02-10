from django import forms
from .models import DTP

class DTPForm(forms.ModelForm):
    class Meta:
        model = DTP
        fields = ['date', 'location', 'name_dri1', 'name_dri2', 'license_plate1', 'license_plate2', 'insurance']

    # Валідація для кожного поля
    def clean_license_plate1(self):
        license_plate1 = self.cleaned_data.get('license_plate1')
        if license_plate1 and len(license_plate1) > 20:
            raise forms.ValidationError("Номер авто водія 1 має бути не більше 20 символів")
        return license_plate1

    def clean_license_plate2(self):
        license_plate2 = self.cleaned_data.get('license_plate2')
        if license_plate2 and len(license_plate2) > 20:
            raise forms.ValidationError("Номер авто водія 2 має бути не більше 20 символів")
        return license_plate2

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date > datetime.date.today():
            raise forms.ValidationError("Дата не може бути в майбутньому")
        return date
