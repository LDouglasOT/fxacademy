from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Testimonial, Purchase, CommunityPost
from datetime import date

def homepage(request):
    testimonials = [
        {'name': 'John Doe', 'message': 'This platform has transformed my trading!', 'date': date(2023, 10, 15)},
        {'name': 'Jane Smith', 'message': 'Accurate signals and great education.', 'date': date(2023, 9, 20)},
        {'name': 'Mike Johnson', 'message': 'Highly recommend for beginners.', 'date': date(2023, 8, 5)},
        {'name': 'Sarah Wilson', 'message': 'Professional and reliable service.', 'date': date(2023, 7, 12)},
    ]
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'homepage.html', context)

def pricing(request):
    subscription_tiers = [
        {
            'name': 'Basic',
            'price': '$50',
            'benefits': ['Zoom lessons link updates', 'Community access'],
            'url': 'classes_enroll'  # Assuming basic is for lessons
        },
        {
            'name': 'Standard',
            'price': '$100',
            'benefits': ['Lessons and signals', 'Community access'],
            'url': 'signals_purchase'  # Assuming standard includes signals
        },
        {
            'name': 'Premium',
            'price': '$500',
            'benefits': ['Lessons, signals, and bots', 'Community access'],
            'url': 'signals_purchase'  # Premium includes signals and more
        }
    ]
    context = {
        'subscription_tiers': subscription_tiers,
    }
    return render(request, 'pricing.html', context)

def signals_purchase(request):
    if request.method == 'POST':
        # Mock payment processing
        messages.success(request, 'Thank You! Your subscription is pending.')
        return redirect('signals_purchase')
    context = {}
    return render(request, 'signals_purchase.html', context)

def classes_enroll(request):
    context = {}
    return render(request, 'classes_enroll.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
        
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    purchases = Purchase.objects.filter(user=request.user)
    community_posts = CommunityPost.objects.filter(user=request.user)
    context = {
        'purchases': purchases,
        'community_posts': community_posts,
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('homepage')
