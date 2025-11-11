from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Subscription(models.Model):
    """Model for managing user subscription levels and access"""
    ACCOUNT_TYPES = [
        ('free', 'Free'),
        ('basic', 'Basic - $50'),
        ('standard', 'Standard - $100'),
        ('premium', 'Premium - $500'),
        ('bots', 'Bots Account - Setup Fee $100'),
    ]
    
    ACCESS_LEVELS = [
        ('telegram', 'Telegram Only'),
        ('signals', 'Signals & Telegram'),
        ('bots', 'Bots & Signals & Telegram'),
        ('all', 'Full Access (Signals, Bots, Classes)'),
    ]
    
    name = models.CharField(max_length=50)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVELS, default='telegram')
    features = models.TextField(help_text="List of features included in this subscription")
    can_access_signals = models.BooleanField(default=False)
    can_access_bots = models.BooleanField(default=False)
    can_access_classes = models.BooleanField(default=False)
    can_access_community = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended user profile with subscription information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    bots_setup_fee_paid = models.BooleanField(default=False)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    is_premium_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Email verification fields
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, unique=True, blank=True, null=True)
    email_verification_sent = models.DateTimeField(null=True, blank=True)
    email_verification_expires = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.subscription.name if self.subscription else 'No subscription'}"
    
    @property
    def has_access_to_signals(self):
        if not self.subscription:
            return False
        return self.subscription.can_access_signals or self.is_premium_user
    
    @property
    def has_access_to_bots(self):
        if not self.subscription:
            return False
        return self.subscription.can_access_bots or self.is_premium_user
    
    @property
    def has_access_to_classes(self):
        if not self.subscription:
            return False
        return self.subscription.can_access_classes or self.is_premium_user

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.date}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    bots_setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, default='pending')
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.subscription:
            return f"{self.user.username} - {self.subscription.name}"
        else:
            return f"{self.user.username} - Bots Setup Fee"

class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
