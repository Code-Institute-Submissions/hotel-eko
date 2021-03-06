from django.urls import path
from . import views

urlpatterns = [
    path('stay/', views.all_stay_services, name='all_stay_services'),
    path('relax/', views.all_relax_services, name='all_relax_services'),
    path('eat/', views.all_eat_services, name='all_eat_services'),
    path('<int:service_id>/', views.service_detail, name='service_detail'),
]
