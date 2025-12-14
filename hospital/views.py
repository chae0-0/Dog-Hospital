from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import date
from .models import *
from .forms import *

# 1. 메인 화면 (대시보드)
def dashboard(request):
    today = date.today()
    
    # 오늘의 예약 현황
    today_appointments = Appointment.objects.filter(date=today).order_by('time')
    
    # 현재 대기 환자
    waiting_patients = Appointment.objects.filter(date=today, status='waiting')
    
    # 진료 현황 요약
    completed_count = Appointment.objects.filter(date=today, status='completed').count()
    
    # 예상 매출 (수납 완료된 건들의 총합)
    total_sales = Payment.objects.filter(paid_at__date=today, is_paid=True).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
    
    context = {
        'today_appointments': today_appointments,
        'waiting_patients': waiting_patients,
        'completed_count': completed_count,
        'total_sales': total_sales,
    }
    return render(request, 'hospital/dashboard.html', context)

# 2. 원무/접수 - 검색 및 등록
def reception_index(request):
    query = request.GET.get('q')
    search_results = []
    
    if query:
        # 보호자 이름 또는 전화번호로 검색
        search_results = Owner.objects.filter(Q(name__contains=query) | Q(phone__contains=query))
        
    return render(request, 'hospital/reception_list.html', {'search_results': search_results})

def register_new_patient(request):
    # 보호자 + 동물 통합 등록
    if request.method == 'POST':
        owner_form = OwnerForm(request.POST)
        animal_form = AnimalForm(request.POST)
        if owner_form.is_valid() and animal_form.is_valid():
            owner = owner_form.save()
            animal = animal_form.save(commit=False)
            animal.owner = owner # 외래키 연결
            animal.save()
            return redirect('reception_index')
    else:
        owner_form = OwnerForm()
        animal_form = AnimalForm()
        
    return render(request, 'hospital/register.html', {'owner_form': owner_form, 'animal_form': animal_form})

def check_in(request, appointment_id):
    # 접수 처리: 예약 상태를 '진료대기'로 변경
    appt = get_object_or_404(Appointment, id=appointment_id)
    appt.status = 'waiting'
    appt.save()
    return redirect('dashboard')

# 3. 진료실
def consultation_room(request, appointment_id):
    appt = get_object_or_404(Appointment, id=appointment_id)
    animal = appt.animal
    
    # 과거 이력 (이전 진료 기록)
    history = MedicalRecord.objects.filter(appointment__animal=animal).exclude(appointment=appt).order_by('-created_at')
    
    if request.method == 'POST':
        record_form = MedicalRecordForm(request.POST)
        if record_form.is_valid():
            # 진료 기록 저장
            record = record_form.save(commit=False)
            record.appointment = appt
            record.vet = appt.vet
            record.save()
            
            # 진료 상태 변경 -> 진료완료
            appt.status = 'completed'
            appt.save()
            
            return redirect('medical_detail', record_id=record.id)
    else:
        record_form = MedicalRecordForm()
        
        # 진료 중 상태로 변경
        if appt.status == 'waiting':
            appt.status = 'in_progress'
            appt.save()

    return render(request, 'hospital/consultation.html', {
        'appt': appt,
        'history': history,
        'record_form': record_form
    })

# 4. 자산 및 재고 관리
def inventory_list(request):
    medicines = Medicine.objects.all()
    tools = MedicalTool.objects.all()
    return render(request, 'hospital/inventory.html', {'medicines': medicines, 'tools': tools})

# 5. 수납
def billing_process(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    
    # 총 진료비 계산 (기본료 + 오더 항목 합계)
    total_cost = 0
    for detail in record.details.all():
        total_cost += detail.treatment.price
        
    if request.method == 'POST':
        # 결제 처리
        payment, created = Payment.objects.get_or_create(record=record, defaults={'total_amount': total_cost})
        payment.paid_amount = total_cost
        payment.payment_method = request.POST.get('method', 'card')
        payment.is_paid = True
        payment.paid_at = timezone.now()
        payment.save()
        return redirect('dashboard')
        
    return render(request, 'hospital/billing.html', {'record': record, 'total_cost': total_cost})