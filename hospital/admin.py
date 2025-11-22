from django.contrib import admin

from django.contrib import admin
# models.py에 있는 모든 클래스를 가져온다는 뜻입니다.
from .models import * # 1. 기초 정보 등록
admin.site.register(Owner)
admin.site.register(Breed)
admin.site.register(Status)
admin.site.register(Veterinarian)
admin.site.register(Medication)
admin.site.register(Treatment)
admin.site.register(Vaccination)

# 2. 핵심 정보 등록
admin.site.register(Animal)

# 3. 진료 및 상세 내역 등록
admin.site.register(MedicalRecord)
admin.site.register(MedicationDetail)
admin.site.register(TreatmentDetail)
admin.site.register(VaccinationDetail)