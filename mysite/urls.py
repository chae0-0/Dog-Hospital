from django.contrib import admin
from django.urls import path, include  # <-- 여기 'include'가 추가됐어요!

urlpatterns = [
    path('admin/', admin.site.urls),
    # 아래 줄이 중요해요! hospital 앱의 주소록을 연결해주는 역할입니다.
    path('', include('hospital.urls')), 
]