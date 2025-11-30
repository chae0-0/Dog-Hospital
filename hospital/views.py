from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Sum, Q
from datetime import date
from .models import Animal, MedicalRecord
from .forms import AnimalForm

#1. 동물 목록 조회
def animal_list(request):
    query = request.GET.get('search')
    if query:
        # 이름(name)이나 보호자 이름(owner_name)에 검색어가 포함되면 찾기
        animals = Animal.objects.filter(
            Q(name__icontains=query) | Q(owner__name__icontains=query)
        )
    else:
        animals = Animal.objects.all()
    
    return render(request, 'hospital/animal_list.html', {'animals': animals})

#2. 동물 상세 조회 (그대로 두세요!)
def animal_detail(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    return render(request, 'hospital/animal_detail.html', {'animal': animal})

#3. 대시보드 (통계)
def dashboard(request):
    total_animals = Animal.objects.count()
    today_records = MedicalRecord.objects.filter(visit_date__date=date.today()).count()

    total_revenue_data = MedicalRecord.objects.aggregate(Sum('cost'))
    total_revenue = total_revenue_data['cost__sum'] or 0

    context = {
        'total_animals': total_animals,
        'today_records': today_records,
        'total_revenue': total_revenue,
    }
    return render(request, 'hospital/dashboard.html', context)

# 4. 동물 등록
def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('animal_list')
    else:
        form = AnimalForm()
    
    return render(request, 'hospital/animal_form.html', {'form': form})