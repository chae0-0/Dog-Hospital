from django.db import models
from django.utils import timezone

# 1. 기초 정보 (수의사, 보호자, 품종, 동물)

class Vet(models.Model):
    name = models.CharField(max_length=50, verbose_name="수의사명")
    contact = models.CharField(max_length=20, verbose_name="연락처")
    
    def __str__(self):
        return self.name

class Owner(models.Model):
    name = models.CharField(max_length=50, verbose_name="보호자명")
    phone = models.CharField(max_length=20, unique=True, verbose_name="전화번호")
    address = models.TextField(verbose_name="주소")
    email = models.EmailField(blank=True, null=True, verbose_name="이메일")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

class Breed(models.Model):
    name = models.CharField(max_length=50, verbose_name="품종명")
    
    def __str__(self):
        return self.name

class Animal(models.Model):
    GENDER_CHOICES = [('M', '수컷'), ('F', '암컷')]
    
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='animals', verbose_name="보호자")
    name = models.CharField(max_length=50, verbose_name="동물명")
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True, verbose_name="품종")
    birth_date = models.DateField(null=True, blank=True, verbose_name="생년월일")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="성별")
    is_neutered = models.BooleanField(default=False, verbose_name="중성화 여부")
    
    def __str__(self):
        return self.name


# 2. 자산 및 기준 정보 (약품, 백신, 기구, 치료항목)

class Medicine(models.Model):
    """약품 정보 (ERD: 약품)"""
    name = models.CharField(max_length=100, verbose_name="약품명")
    manufacturer = models.CharField(max_length=100, blank=True, verbose_name="제조사")
    stock = models.IntegerField(default=0, verbose_name="재고 수량")
    unit = models.CharField(max_length=10, verbose_name="단위") # 예: 정, ml
    expiry_date = models.DateField(null=True, blank=True, verbose_name="유통기한")
    price = models.IntegerField(default=0, verbose_name="단가")
    
    def __str__(self):
        return self.name

class Vaccine(models.Model):
    """백신 정보 (ERD: 접종 - 기준 정보)"""
    name = models.CharField(max_length=100, verbose_name="백신명")
    manufacturer = models.CharField(max_length=100, blank=True, verbose_name="제약회사")
    stock = models.IntegerField(default=0, verbose_name="재고 수량")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="유통기한")
    price = models.IntegerField(verbose_name="접종 비용")

    def __str__(self):
        return self.name

class MedicalTool(models.Model):
    """의료기구 정보 (ERD: 치료기구)"""
    name = models.CharField(max_length=100, verbose_name="기구명") # ERD의 기구명 테이블 통합
    code = models.CharField(max_length=50, blank=True, verbose_name="관리코드/일련번호")
    stock = models.IntegerField(default=1, verbose_name="보유 수량")
    manufacturer = models.CharField(max_length=100, blank=True, verbose_name="제조사")
    
    def __str__(self):
        return self.name

class TreatmentInfo(models.Model):
    """치료 기준 정보 (ERD: 치료 - 기준 정보)"""
    name = models.CharField(max_length=100, verbose_name="치료/검사명")
    price = models.IntegerField(verbose_name="기준 비용")
    
    def __str__(self):
        return self.name


# 3. 예약 및 접수

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('reserved', '예약중'),
        ('waiting', '진료대기'),
        ('in_progress', '진료중'),
        ('completed', '진료완료'),
        ('canceled', '취소'),
    ]

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="보호자")
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="환자")
    vet = models.ForeignKey(Vet, on_delete=models.SET_NULL, null=True, verbose_name="담당 수의사")
    date = models.DateField(verbose_name="예약 날짜")
    time = models.TimeField(verbose_name="예약 시간")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved', verbose_name="상태")
    reason = models.TextField(verbose_name="내원 사유")
    
    def __str__(self):
        return f"[{self.get_status_display()}] {self.animal.name} - {self.date}"


# 4. 진료 기록

class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_record')
    vet = models.ForeignKey(Vet, on_delete=models.PROTECT, verbose_name="담당 수의사")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="진료일시")
    
    weight = models.FloatField(verbose_name="체중(kg)")
    temperature = models.FloatField(verbose_name="체온")
    symptom = models.TextField(verbose_name="증상 상세")
    diagnosis = models.CharField(max_length=100, verbose_name="진단명")
    test_result = models.TextField(verbose_name="검사 결과", blank=True, help_text="예: 골절, 신장 수치 등")

    def __str__(self):
        return f"진료기록 - {self.appointment.animal.name} ({self.created_at.date()})"


# 5. 진료 상세 내역

class MedicalDetail(models.Model):
    #일반 치료 내역 (치료_상세)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='treatments')
    treatment = models.ForeignKey(TreatmentInfo, on_delete=models.PROTECT, verbose_name="치료항목")
    description = models.TextField(blank=True, verbose_name="치료 메모")
    
    def __str__(self):
        return f"{self.treatment.name}"

class Prescription(models.Model):
    #약물 처방 내역 (약물처방_상세)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT, verbose_name="처방 약품")
    amount = models.IntegerField(default=1, verbose_name="처방 수량")
    description = models.TextField(blank=True, verbose_name="복용법/기간")
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.medicine.stock -= self.amount
            self.medicine.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine.name} ({self.amount})"

class VaccinationRecord(models.Model):
    #예방 접종 내역 (접종_상세)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.PROTECT, verbose_name="백신")
    description = models.TextField(blank=True, verbose_name="접종 메모")
    next_due_date = models.DateField(null=True, blank=True, verbose_name="다음 접종 예정일")
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.vaccine.stock -= 1
            self.vaccine.save()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.vaccine.name

class ToolUsage(models.Model):
    #기구 사용 내역 (기구사용내역)
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='tool_usages')
    tool = models.ForeignKey(MedicalTool, on_delete=models.PROTECT, verbose_name="사용 기구")
    count = models.IntegerField(default=1, verbose_name="사용 횟수/수량")
    description = models.TextField(blank=True, verbose_name="비고")

    def __str__(self):
        return f"{self.tool.name} 사용"


# 6. 수납

class Payment(models.Model):
    METHOD_CHOICES = [('card', '카드'), ('cash', '현금')]
    record = models.OneToOneField(MedicalRecord, on_delete=models.CASCADE, related_name='payment')
    total_amount = models.IntegerField(verbose_name="청구 금액")
    paid_amount = models.IntegerField(default=0, verbose_name="실 수납 금액")
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='card', verbose_name="결제 수단")
    is_paid = models.BooleanField(default=False, verbose_name="수납 완료 여부")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="수납 일시")

    def __str__(self):
        return f"{self.record.appointment.animal.name} - {self.total_amount}원"