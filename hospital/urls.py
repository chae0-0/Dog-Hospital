from django.urls import path
from . import views

urlpatterns = [
    # 1. 대시보드
    path('', views.dashboard, name='dashboard'),

    # 2. 접수/원무
    path('reception/', views.reception_index, name='reception_index'),
    path('reception/register/', views.register_new_patient, name='register_new_patient'),
    path('appointment/<int:appointment_id>/checkin/', views.check_in, name='check_in'),
    path('animals/', views.animal_list, name='animal_list'),


    # 3. 진료실
    path('consultation/<int:appointment_id>/', views.consultation_room, name='consultation_room'),
    
    # 4. 재고
    path('inventory/', views.inventory_list, name='inventory_list'),
    
    # 5. 수납
    path('billing/<int:record_id>/', views.billing_process, name='billing_process'),
]