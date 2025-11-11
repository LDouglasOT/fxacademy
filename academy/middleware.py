from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            try:
                from .models import UserProfile
                profile = request.user.profile
                
                # Skip email verification for certain URLs
                exempt_urls = [
                    'email_verification_pending',
                    'email_verification_success', 
                    'verify_email',
                    'resend_verification_email',
                    'logout',
                    'email_webhook'
                ]
                
                current_url = request.resolver_match.url_name if request.resolver_match else None
                
                if current_url not in exempt_urls:
                    # Check if email is verified
                    if not profile.is_email_verified:
                        messages.warning(request, 'Please verify your email address to access this feature.')
                        return redirect('email_verification_pending')
                        
            except UserProfile.DoesNotExist:
                # Create profile if it doesn't exist (shouldn't happen normally)
                from .models import Subscription
                try:
                    free_subscription = Subscription.objects.get(account_type='free')
                    UserProfile.objects.create(user=request.user, subscription=free_subscription)
                except Subscription.DoesNotExist:
                    pass
            except Exception:
                # If there's any other error, allow access but log it
                pass

        response = self.get_response(request)
        return response