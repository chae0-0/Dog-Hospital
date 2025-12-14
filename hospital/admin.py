from django.contrib import admin
from .models import (
    Vet, Owner, Breed, Animal, 
    Medicine, Vaccine, MedicalTool, TreatmentInfo, 
    Appointment, MedicalRecord, 
    MedicalDetail, Prescription, VaccinationRecord, ToolUsage, 
    Payment
)

# 1. 기초 정보 관리
@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at')
    search_fields = ('name', 'phone')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'breed', 'gender', 'birth_date')
    search_fields = ('name', 'owner__name')
    list_filter = ('breed', 'gender')

@admin.register(Vet)
class VetAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact')

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    pass

# 2. 자산 및 기준 정보
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'stock', 'unit', 'expiry_date')
    search_fields = ('name',)
    list_filter = ('manufacturer',)

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'stock', 'expiry_date')

@admin.register(MedicalTool)
class MedicalToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'manufacturer')

@admin.register(TreatmentInfo)
class TreatmentInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

# 3. 예약 및 진료 관리
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'owner', 'animal', 'vet', 'status')
    list_filter = ('status', 'date', 'vet')
    search_fields = ('owner__name', 'animal__name')

class PrescriptionInline(admin.TabularInline):
    model = Prescription
    extra = 0

class MedicalDetailInline(admin.TabularInline):
    model = MedicalDetail
    extra = 0

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'vet', 'diagnosis', 'created_at')
    inlines = [MedicalDetailInline, PrescriptionInline]

# 4. 상세 내역 및 수납
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('record', 'total_amount', 'paid_amount', 'is_paid', 'paid_at')
    list_filter = ('is_paid', 'payment_method')

# 나머지 상세 테이블 등록
admin.site.register(MedicalDetail)
admin.site.register(Prescription)
admin.site.register(VaccinationRecord)
admin.site.register(ToolUsage)