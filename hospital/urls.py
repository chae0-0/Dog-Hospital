from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('reception/', views.reception_index, name='reception_index'),
    path('reception/register/', views.register_new_patient, name='register_new_patient'),
    path('appointment/<int:appointment_id>/checkin/', views.check_in, name='check_in'),

    # 수의사 전용
    path('doctor/patients/', views.my_patient_list, name='my_patient_list'),
    path('consultation/<int:appointment_id>/', views.consultation_room, name='consultation_room'),

    path('inventory/', views.inventory_list, name='inventory_list'),
    path('billing/', views.billing_search, name='billing_search'),
    path('billing/process/<int:record_id>/', views.billing_process, name='billing_process'),
]