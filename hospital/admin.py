from django.contrib import admin
from .models import *

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'breed')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'owner', 'animal', 'status')

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'expiry_date')

@admin.register(MedicalTool)
class MedicalToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'stock') # status 확인 가능

@admin.register(Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'vendor')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'item_type')


admin.site.register(Vet)
admin.site.register(Breed)
admin.site.register(Vaccine)
admin.site.register(TreatmentInfo)
admin.site.register(MedicalRecord)
admin.site.register(MedicalDetail)
admin.site.register(Prescription)
admin.site.register(VaccinationRecord)
admin.site.register(ToolUsage)
admin.site.register(Payment)