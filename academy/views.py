from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Testimonial, Purchase, CommunityPost, Subscription, UserProfile
from .forms import CustomUserCreationForm
from .email_service import EmailService
from datetime import date, datetime

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
    # Fetch active subscriptions from database
    subscriptions = Subscription.objects.filter(is_active=True).order_by('price')
    
    context = {
        'subscriptions': subscriptions,
    }
    return render(request, 'pricing.html', context)

def signals_purchase(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, 'Please complete your profile setup.')
            return redirect('dashboard')
    
    # Handle POST request for payment processing
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to purchase a subscription.')
            return redirect('login')
        
        # Mock payment processing - in real implementation, integrate with payment processor
        messages.success(request, 'Thank You! Your subscription is pending verification.')
        return redirect('signals_purchase')
    
    # For GET request, check user access
    context = {}
    if user_profile:
        # User is logged in, check their access level
        if user_profile.has_access_to_signals:
            # User has access to signals
            context['has_access'] = True
            context['subscription_name'] = user_profile.subscription.name
        else:
            # User doesn't have access, show upgrade prompt
            context['has_access'] = False
            context['current_subscription'] = user_profile.subscription.name
            # Get available upgrades
            available_upgrades = Subscription.objects.filter(
                can_access_signals=True,
                price__gt=user_profile.subscription.price if user_profile.subscription else 0
            ).order_by('price')
            context['available_upgrades'] = available_upgrades
    else:
        # User not logged in, show login prompt
        context['show_login_prompt'] = True
    
    return render(request, 'signals_purchase.html', context)

def classes_enroll(request):
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            messages.error(request, 'Please complete your profile setup.')
            return redirect('dashboard')
    
    context = {}
    if user_profile:
        if user_profile.has_access_to_classes:
            # User has access to classes
            context['has_access'] = True
            context['subscription_name'] = user_profile.subscription.name
        else:
            # User doesn't have access, show upgrade prompt
            context['has_access'] = False
            context['current_subscription'] = user_profile.subscription.name
            # Get available upgrades that include classes
            available_upgrades = Subscription.objects.filter(
                can_access_classes=True,
                price__gt=user_profile.subscription.price if user_profile.subscription else 0
            ).order_by('price')
            context['available_upgrades'] = available_upgrades
    else:
        context['show_login_prompt'] = True
    
    return render(request, 'classes_enroll.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Please provide both email and password.')
            return render(request, 'login.html')
        
        # Find user by email
        try:
            user = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
        
        # Authenticate with username and password
        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            # Validate email using Mailer API
            email_validation = EmailService.validate_email(email)
            
            if not email_validation.get('success', False):
                messages.error(request, 'Please enter a valid email address.')
                return render(request, 'signup.html', {'form': form})
            
            # Create user account
            user = form.save()
            
            # Create user profile with free subscription
            try:
                free_subscription = Subscription.objects.get(account_type='free')
                user_profile = UserProfile.objects.create(
                    user=user,
                    subscription=free_subscription
                )
            except Subscription.DoesNotExist:
                messages.error(request, 'System error. Please contact support.')
                user.delete()  # Clean up user if profile creation fails
                return render(request, 'signup.html', {'form': form})
            
            # Send verification email
            if EmailService.send_verification_email(user, user_profile):
                messages.success(request, 'Account created! Please check your email to verify your account.')
                return redirect('email_verification_pending')
            else:
                messages.warning(request, 'Account created but verification email failed to send. Please contact support.')
                return redirect('email_verification_pending')
                
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        free_subscription = Subscription.objects.get(account_type='free')
        user_profile = UserProfile.objects.create(user=request.user, subscription=free_subscription)
    
    purchases = Purchase.objects.filter(user=request.user)
    community_posts = CommunityPost.objects.filter(user=request.user)
    
    context = {
        'purchases': purchases,
        'community_posts': community_posts,
        'user_profile': user_profile,
        'has_access_to_signals': user_profile.has_access_to_signals,
        'has_access_to_bots': user_profile.has_access_to_bots,
        'has_access_to_classes': user_profile.has_access_to_classes,
        'current_subscription': user_profile.subscription,
        'available_upgrades': Subscription.objects.filter(
            price__gt=user_profile.subscription.price
        ).order_by('price') if user_profile.subscription else None,
    }
    return render(request, 'dashboard.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        
        if not title or not content:
            messages.error(request, 'Both title and content are required.')
            return redirect('dashboard')
        
        try:
            post = CommunityPost.objects.create(
                user=request.user,
                title=title,
                content=content
            )
            messages.success(request, 'Post created successfully!')
        except Exception as e:
            messages.error(request, 'Error creating post. Please try again.')
        
        return redirect('dashboard')
    
    # GET request - show create post form
    return render(request, 'create_post.html')

# Email verification views
def email_verification_pending(request):
    """Show email verification pending page"""
    return render(request, 'email_verification_pending.html')

def verify_email_success(request):
    """Show email verification success page"""
    return render(request, 'email_verification_success.html')

def verify_email(request):
    """Handle email verification via token"""
    token = request.GET.get('token', '')
    
    if not token:
        messages.error(request, 'Invalid verification link.')
        return redirect('email_verification_pending')
    
    result = EmailService.verify_email_token(token)
    
    if result['success']:
        # Auto-login the user
        user = result['user']
        login(request, user)
        messages.success(request, 'Email verified successfully! Welcome to Forex Academy!')
        return redirect('email_verification_success')
    else:
        messages.error(request, result['error'])
        return redirect('email_verification_pending')

@login_required
def resend_verification_email(request):
    """Resend verification email"""
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        if profile.is_email_verified:
            messages.info(request, 'Your email is already verified.')
            return redirect('dashboard')
        
        # Check if we can send a new verification (rate limiting)
        if profile.email_verification_sent:
            time_diff = datetime.now() - profile.email_verification_sent
            if time_diff.total_seconds() < 300:  # 5 minutes
                messages.warning(request, 'Please wait 5 minutes before requesting another verification email.')
                return redirect('email_verification_pending')
        
        if EmailService.send_verification_email(user, profile):
            messages.success(request, 'Verification email sent! Please check your inbox.')
        else:
            messages.error(request, 'Failed to send verification email. Please try again.')
        
        return redirect('email_verification_pending')
    
    return redirect('email_verification_pending')

def email_webhook(request):
    """Webhook endpoint for email verification (for external email services)"""
    if request.method == 'POST':
        try:
            data = request.json
            email = data.get('email')
            verified = data.get('verified', False)
            
            if email and verified:
                try:
                    user = User.objects.get(email=email)
                    profile = user.profile
                    profile.is_email_verified = True
                    profile.email_verification_token = None
                    profile.save()
                    
                    return JsonResponse({'status': 'success', 'message': 'Email verified via webhook'})
                except User.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
            
            return JsonResponse({'status': 'error', 'message': 'Invalid webhook data'}, status=400)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def logout_view(request):
    logout(request)
    return redirect('homepage')
