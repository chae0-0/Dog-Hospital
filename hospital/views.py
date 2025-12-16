from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import date
from .models import *
from .forms import *



# 0. 수의사 (로그인/로그아웃)

def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        try:
            vet = Vet.objects.get(contact=phone)
            request.session['is_vet'] = True
            request.session['vet_id'] = vet.id
            request.session['vet_name'] = vet.name
            return redirect('dashboard')
        except Vet.DoesNotExist:
            return render(request, 'hospital/login.html', {'error': '등록된 수의사 연락처가 아닙니다.'})
    return render(request, 'hospital/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('dashboard')



# 1. 메인 화면 (대시보드)

def dashboard(request):
    today = date.today()
    today_appointments = Appointment.objects.filter(date=today).order_by('time')
    waiting_patients = Appointment.objects.filter(date=today, status='waiting')
    completed_count = Appointment.objects.filter(date=today, status='completed').count()


    # 오늘 날짜에 수납 완료된(is_paid=True) 금액의 합계. 없으면 0.
    total_sales = Payment.objects.filter(paid_at__date=today, is_paid=True).aggregate(Sum('paid_amount'))[
                      'paid_amount__sum'] or 0

    context = {
        'today_appointments': today_appointments,
        'waiting_patients': waiting_patients,
        'completed_count': completed_count,
        'total_sales': total_sales,  # 템플릿으로 전달
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
    context = {'search_results': search_results, 'today_appointments': today_appointments,
               'appointment_form': appointment_form}
    return render(request, 'hospital/reception_list.html', context)


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


def check_in(request, appointment_id):
    appt = get_object_or_404(Appointment, id=appointment_id)
    appt.status = 'waiting'
    appt.save()
    return redirect('reception_index')



# 3. 진료실

def my_patient_list(request):
    if not request.session.get('is_vet'): return redirect('login')
    vet_id = request.session.get('vet_id')
    today = date.today()
    my_patients = Appointment.objects.filter(vet_id=vet_id, date=today, status__in=['waiting', 'in_progress']).order_by(
        'time')
    history_list = Appointment.objects.filter(vet_id=vet_id, status='completed').order_by('-date', '-time')[:10]
    return render(request, 'hospital/my_patient_list.html', {'my_patients': my_patients, 'history_list': history_list})


def consultation_room(request, appointment_id):
    if not request.session.get('is_vet'): return redirect('login')
    appt = get_object_or_404(Appointment, id=appointment_id)
    record, created = MedicalRecord.objects.get_or_create(appointment=appt,
                                                          defaults={'vet': appt.vet, 'weight': 0, 'temperature': 0})
    if appt.status == 'waiting':
        appt.status = 'in_progress'
        appt.save()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save_chart':
            form = MedicalRecordForm(request.POST, instance=record)
            if form.is_valid(): form.save()
        elif action == 'add_treatment':
            treatment_id = request.POST.get('treatment_id')
            if treatment_id:
                treatment = get_object_or_404(TreatmentInfo, id=treatment_id)
                MedicalDetail.objects.create(record=record, treatment=treatment)
        elif action == 'delete_treatment':
            detail_id = request.POST.get('detail_id')
            MedicalDetail.objects.filter(id=detail_id).delete()
        elif action == 'finish':
            form = MedicalRecordForm(request.POST, instance=record)
            if form.is_valid(): form.save()
            appt.status = 'completed'
            appt.save()
            return redirect('my_patient_list')
        return redirect('consultation_room', appointment_id=appt.id)

    history = MedicalRecord.objects.filter(appointment__animal=appt.animal).exclude(id=record.id).order_by(
        '-created_at')
    record_form = MedicalRecordForm(instance=record)
    all_treatments = TreatmentInfo.objects.all()
    added_treatments = record.treatments.all()
    context = {'appt': appt, 'record': record, 'history': history, 'record_form': record_form,
               'all_treatments': all_treatments, 'added_treatments': added_treatments}
    return render(request, 'hospital/consultation.html', context)



# 4. 재고 및 수납

def inventory_list(request):
    if not request.session.get('is_vet'): return redirect('login')
    medicines = Medicine.objects.all()
    consumables = Consumable.objects.all()
    tools = MedicalTool.objects.all()
    vendors = Vendor.objects.all()

    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')
        if action == 'restock_med':
            amount = int(request.POST.get('amount', 0))
            item = get_object_or_404(Medicine, id=item_id)
            item.stock += amount
            item.save()
        elif action == 'restock_consumable':
            amount = int(request.POST.get('amount', 0))
            item = get_object_or_404(Consumable, id=item_id)
            item.stock += amount
            item.save()
        elif action == 'update_tool_status':
            new_status = request.POST.get('status')
            item = get_object_or_404(MedicalTool, id=item_id)
            item.status = new_status
            item.save()
        elif action == 'add_vendor':
            Vendor.objects.create(name=request.POST.get('name'), contact=request.POST.get('contact'),
                                  item_type=request.POST.get('item_type'))
        return redirect('inventory_list')

    context = {'medicines': medicines, 'consumables': consumables, 'tools': tools, 'vendors': vendors}
    return render(request, 'hospital/inventory.html', context)


def billing_search(request):
    query = request.GET.get('q')
    unpaid_records = []
    if query:
        owners = Owner.objects.filter(Q(name__contains=query) | Q(phone__contains=query))
        records = MedicalRecord.objects.filter(appointment__owner__in=owners).filter(
            Q(payment__isnull=True) | Q(payment__is_paid=False)).order_by('-created_at')
        for rec in records:
            total = 0
            for treat in rec.treatments.all(): total += treat.treatment.price
            for vac in rec.vaccinations.all(): total += vac.vaccine.price
            for med in rec.prescriptions.all(): total += med.medicine.price * med.amount
            unpaid_records.append({'id': rec.id, 'date': rec.created_at, 'animal_name': rec.appointment.animal.name,
                                   'owner_name': rec.appointment.owner.name, 'diagnosis': rec.diagnosis,
                                   'total_amount': total})
    return render(request, 'hospital/billing_search.html', {'unpaid_records': unpaid_records, 'query': query})


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
    context = {'record': record, 'treatments': treatments, 'vaccines': vaccines, 'medications': medications,
               'treat_total': treat_total, 'vac_total': vac_total, 'med_total': med_total, 'total_cost': total_cost,
               'query': query}
    return render(request, 'hospital/billing.html', context)