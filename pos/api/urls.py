from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "api"

urlpatterns = [
    #path('api/v1/login', LoginView.as_view(),),
    #path('api/v1/logout', LogoutView.as_view(),),
    #path('api/v1/Register', RegisterWaitressAPI.as_view(),),
     path('api/layanan', views.LayananListAPIView.as_view()),
     path('api/layanan/<int:pk>', views.LayananDetailAPIView.as_view()),
     path('api/jenis-pembayaran', views.JenisPembayaranListAPIView.as_view()),
     path('api/jenis-pembayaran/<int:pk>', views.JenisPembayaranDetailAPIView.as_view()),
     path('api/register', views.RegisterUserAPIView.as_view()),
     path('api/login', views.LoginView.as_view()),
     path('api/pembayaran/', views.PembayaranListCreateAPIView.as_view(), name='pembayaran-list'),
     path('api/pembayaran/<int:pk>/', views.PembayaranListCreateAPIView.as_view(), name='pembayaran-detail'),  # Tetap biarkan
     path('api/pembayaran-crud/<int:pk>/', views.PembayaranRetrieveUpdateDestroyAPIView.as_view(), name='pembayaran-crud'),
]
