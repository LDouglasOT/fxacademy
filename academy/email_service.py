import requests
import uuid
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.conf import settings
from .models import UserProfile

class EmailService:
    API_KEY = 'cda11013-d8a3-43f5-8140-0cfb7a7e306f'
    BASE_URL = 'https://api.mails.so/v1'
    
    @classmethod
    def validate_email(cls, email):
        """Validate email using Mailer API"""
        try:
            url = f'{cls.BASE_URL}/validate'
            headers = {
                'x-mails-api-key': cls.API_KEY,
                'Content-Type': 'application/json'
            }
            data = {
                'email': email
            }
            
            response = requests.post(url, headers=headers, json=data)
            return response.json()
        except Exception as e:
            print(f"Email validation error: {e}")
            return {'success': False, 'error': 'Validation service unavailable'}
    
    @classmethod
    def send_verification_email(cls, user, profile):
        """Send email verification link"""
        try:
            # Generate verification token
            token = str(uuid.uuid4())
            profile.email_verification_token = token
            profile.email_verification_sent = datetime.now()
            profile.email_verification_expires = datetime.now() + timedelta(hours=24)
            profile.save()
            
            # Build verification URL
            verification_url = f"{settings.SITE_URL}{reverse('verify_email')}?token={token}"
            
            # Create email content
            subject = "Verify Your Email - Forex Academy"
            html_message = render_to_string('email/verification_email.html', {
                'user': user,
                'verification_url': verification_url,
                'expires_hours': 24
            })
            
            # Create plain text version
            plain_message = f"""
Welcome to Forex Academy!

Please verify your email address by clicking the link below:
{verification_url}

This link will expire in 24 hours for security reasons.

If you didn't create this account, please ignore this email.

Best regards,
Forex Academy Team
            """
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
            
            return True
            
        except Exception as e:
            print(f"Email sending error: {e}")
            return False
    
    @classmethod
    def verify_email_token(cls, token):
        """Verify email using the provided token"""
        try:
            profile = UserProfile.objects.get(email_verification_token=token)
            
            # Check if token is expired
            if profile.email_verification_expires and datetime.now() > profile.email_verification_expires:
                return {'success': False, 'error': 'Verification link has expired'}
            
            # Mark as verified
            profile.is_email_verified = True
            profile.email_verification_token = None  # Clear token
            profile.email_verification_expires = None
            profile.save()
            
            return {'success': True, 'user': profile.user}
            
        except UserProfile.DoesNotExist:
            return {'success': False, 'error': 'Invalid verification link'}
        except Exception as e:
            return {'success': False, 'error': 'Verification failed'}
    
    @classmethod
    def resend_verification_email(cls, user):
        """Resend verification email to user"""
        try:
            profile = user.profile
            return cls.send_verification_email(user, profile)
        except Exception as e:
            print(f"Resend verification error: {e}")
            return False