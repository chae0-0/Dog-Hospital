from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import date
from .models import *
from .forms import *


# 1. 메인 화면 (대시보드)
def dashboard(request):
    today = date.today()
    today_appointments = Appointment.objects.filter(date=today).order_by('time')
    waiting_patients = Appointment.objects.filter(date=today, status='waiting')
    completed_count = Appointment.objects.filter(date=today, status='completed').count()

    context = {
        'today_appointments': today_appointments,
        'waiting_patients': waiting_patients,
        'completed_count': completed_count,
    }
    return render(request, 'hospital/dashboard.html', context)


# 2. 원무/접수
def reception_index(request):
    today = date.today()
    query = request.GET.get('q')
    search_results = []
    if query:
        search_results = Owner.objects.filter(Q(name__contains=query) | Q(phone__contains=query))

    today_appointments = Appointment.objects.filter(date=today).order_by('time')

    if request.method == 'POST':
        if request.POST.get('action') == 'create_appt':
            form = AppointmentForm(request.POST)
            animal_id = request.POST.get('animal')
            owner_id = request.POST.get('owner')

            if form.is_valid():
                appt = form.save(commit=False)
                if animal_id: appt.animal_id = animal_id
                if owner_id: appt.owner_id = owner_id
                appt.save()
                return redirect('reception_index')
            else:
                try:
                    appt = form.save(commit=False)
                    if animal_id and owner_id:
                        appt.animal_id = animal_id
                        appt.owner_id = owner_id
                        appt.save()
                        return redirect('reception_index')
                except:
                    pass

    appointment_form = AppointmentForm()
    context = {
        'search_results': search_results,
        'today_appointments': today_appointments,
        'appointment_form': appointment_form,
    }
    return render(request, 'hospital/reception_list.html', context)


# 3. 신규 환자 등록
def register_new_patient(request):
    if request.method == 'POST':
        owner_form = OwnerForm(request.POST)
        animal_form = AnimalForm(request.POST)
        if owner_form.is_valid() and animal_form.is_valid():
            owner = owner_form.save()
            animal = animal_form.save(commit=False)
            animal.owner = owner
            animal.save()
            return redirect('reception_index')
    else:
        owner_form = OwnerForm()
        animal_form = AnimalForm()
    return render(request, 'hospital/register.html', {'owner_form': owner_form, 'animal_form': animal_form})


# 4. 접수 처리
def check_in(request, appointment_id):
    appt = get_object_or_404(Appointment, id=appointment_id)
    appt.status = 'waiting'
    appt.save()
    return redirect('reception_index')


# 5. 진료실
def consultation_room(request, appointment_id):
    appt = get_object_or_404(Appointment, id=appointment_id)
    animal = appt.animal
    history = MedicalRecord.objects.filter(appointment__animal=animal).exclude(appointment=appt).order_by('-created_at')

    if request.method == 'POST':
        record_form = MedicalRecordForm(request.POST)
        if record_form.is_valid():
            record = record_form.save(commit=False)
            record.appointment = appt
            record.vet = appt.vet
            record.save()
            appt.status = 'completed'
            appt.save()
            return redirect('dashboard')
    else:
        record_form = MedicalRecordForm()
        if appt.status == 'waiting':
            appt.status = 'in_progress'
            appt.save()

    return render(request, 'hospital/consultation.html', {
        'appt': appt,
        'history': history,
        'record_form': record_form
    })


# 6. 수납 관리 (검색)
def billing_search(request):
    query = request.GET.get('q')
    unpaid_records = []

    if query:
        owners = Owner.objects.filter(Q(name__contains=query) | Q(phone__contains=query))
        records = MedicalRecord.objects.filter(
            appointment__owner__in=owners
        ).filter(
            Q(payment__isnull=True) | Q(payment__is_paid=False)
        ).order_by('-created_at')

        for rec in records:
            total = 0
            for treat in rec.treatments.all():
                total += treat.treatment.price
            for vac in rec.vaccinations.all():
                total += vac.vaccine.price
            for med in rec.prescriptions.all():
                total += med.medicine.price * med.amount

            unpaid_records.append({
                'id': rec.id,
                'date': rec.created_at,
                'animal_name': rec.appointment.animal.name,
                'owner_name': rec.appointment.owner.name,
                'diagnosis': rec.diagnosis,
                'total_amount': total
            })

    return render(request, 'hospital/billing_search.html', {'unpaid_records': unpaid_records, 'query': query})


# 7. 수납 상세 (조회)
def billing_process(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)

    treatments = record.treatments.all()
    treat_total = sum(t.treatment.price for t in treatments)

    vaccines = record.vaccinations.all()
    vac_total = sum(v.vaccine.price for v in vaccines)

    medications = record.prescriptions.all()
    med_total = sum(m.medicine.price * m.amount for m in medications)

    total_cost = treat_total + vac_total + med_total
    query = request.GET.get('q', '')
    context = {
        'record': record,
        'treatments': treatments,
        'vaccines': vaccines,
        'medications': medications,
        'treat_total': treat_total,
        'vac_total': vac_total,
        'med_total': med_total,
        'total_cost': total_cost,
        'query': query,
    }
    return render(request, 'hospital/billing.html', context)



def animal_medication(request, animal_id):
    return redirect('reception_index')


def animal_vaccination(request, animal_id):
    return redirect('reception_index')


def animal_treatment(request, animal_id):
    return redirect('reception_index')