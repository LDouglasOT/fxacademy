from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('pricing/', views.pricing, name='pricing'),
    path('signals/purchase/', views.signals_purchase, name='signals_purchase'),
    path('classes/enroll/', views.classes_enroll, name='classes_enroll'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
]