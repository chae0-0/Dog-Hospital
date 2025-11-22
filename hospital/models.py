from django.db import models

from django.db import models

# 1. 기초 정보 (기준 정보) 테이블

class Owner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Breed(models.Model):
    breed_id = models.AutoField(primary_key=True)
    breed_name = models.CharField(max_length=50)

    def __str__(self):
        return self.breed_name

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=30)  # 예: 입원, 퇴원, 치료중

    def __str__(self):
        return self.status_name

class Veterinarian(models.Model):
    vet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Medication(models.Model):
    med_id = models.AutoField(primary_key=True)
    med_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=50, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    stock_qty = models.IntegerField(default=0)

    def __str__(self):
        return self.med_name

class Treatment(models.Model):
    treatment_id = models.AutoField(primary_key=True)
    treatment_name = models.CharField(max_length=100)

    def __str__(self):
        return self.treatment_name

class Vaccination(models.Model):
    vaccine_id = models.AutoField(primary_key=True)
    vaccine_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.vaccine_name


# 2. 핵심 엔티티 (동물)

class Animal(models.Model):
    animal_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])

    def __str__(self):
        return f"{self.name} ({self.owner.name})"


# 3. 업무 트랜잭션 (진료 기록)

class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    vet = models.ForeignKey(Veterinarian, on_delete=models.PROTECT)
    
    visit_date = models.DateTimeField(auto_now_add=True) # 생성시 자동 시간 입력
    diagnosis = models.CharField(max_length=500, null=True, blank=True)
    procedure_note = models.TextField(null=True, blank=True)
    cost = models.IntegerField(default=0)

    def __str__(self):
        return f"Record #{self.record_id} - {self.animal.name}"


# 4. 상세 내역 (M:N 관계 해소)

class MedicationDetail(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE) # 진료기록 삭제시 같이 삭제
    medication = models.ForeignKey(Medication, on_delete=models.PROTECT)
    dosage = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)

class TreatmentDetail(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT)
    treat_date = models.DateTimeField()
    note = models.TextField(null=True, blank=True)

class VaccinationDetail(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccination, on_delete=models.PROTECT)
    vac_date = models.DateField()
    next_vac_date = models.DateField(null=True, blank=True)
