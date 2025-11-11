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
    path('dashboard/create-post/', views.create_post, name='create_post'),
    # Email verification URLs
    path('email/verify/', views.verify_email, name='verify_email'),
    path('email/pending/', views.email_verification_pending, name='email_verification_pending'),
    path('email/success/', views.verify_email_success, name='email_verification_success'),
    path('email/resend/', views.resend_verification_email, name='resend_verification_email'),
    path('email/webhook/', views.email_webhook, name='email_webhook'),
    path('logout/', views.logout_view, name='logout'),
]