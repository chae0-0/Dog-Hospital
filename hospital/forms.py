from django import forms
from .models import Animal, MedicalRecord

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'breed', 'owner', 'gender', 'birth_date', 'status']