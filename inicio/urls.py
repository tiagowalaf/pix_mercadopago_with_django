from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('transaction/', views.process_transaction, name='transaction'),
    path('qr_code/', views.show_qr_code, name='show_qr'),
]
