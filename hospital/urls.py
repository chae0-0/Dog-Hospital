from django.urls import path
from . import views

urlpatterns = [
    # 1. 메인(대시보드)
    path('', views.dashboard, name='dashboard'),

    # 2. 원무/접수
    path('reception/', views.reception_index, name='reception_index'),
    path('reception/register/', views.register_new_patient, name='register_new_patient'),

    # 3. 진료실
    path('consultation/<int:appointment_id>/', views.consultation_room, name='consultation_room'),

    # 4. 수납
    path('billing/', views.billing_search, name='billing_search'),
    path('billing/process/<int:record_id>/', views.billing_process, name='billing_process'),  # 실제 결제 처리 화면

    # 5. 접수 처리
    path('appointment/<int:appointment_id>/checkin/', views.check_in, name='check_in'),
]