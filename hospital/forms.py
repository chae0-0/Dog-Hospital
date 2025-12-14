from django import forms
from .models import Owner, Animal, Appointment, MedicalRecord, MedicalDetail

# 1. 통합 등록 (보호자 + 동물)
class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'phone', 'address', 'email']

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'breed', 'birth_date', 'gender', 'is_neutered']

# 2. 예약/접수
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['vet', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

# 3. 진료 차트 작성
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord

        fields = ['weight', 'temperature', 'symptom', 'diagnosis', 'test_result']
        
        widgets = {
            'test_result': forms.Textarea(attrs={'rows': 3, 'placeholder': '검사 결과를 입력하세요 (예: 염증 수치 0.0056)'}),
        }

# 4. 진료 오더(실제로 어떤 치료나 검사를 했는지)
class MedicalDetailForm(forms.ModelForm):
    class Meta:
        model = MedicalDetail
        fields = ['treatment', 'description']