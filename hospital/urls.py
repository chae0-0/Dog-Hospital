from django.urls import path
from . import views

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    
    # 동물 상세 페이지
    path('animal/<int:animal_id>/', views.animal_detail, name='animal_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),      # 대시보드 주소
    path('add/', views.animal_create, name='animal_create'),    # 등록 주소
]