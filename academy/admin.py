from django.contrib import admin
from .models import Testimonial, Purchase, CommunityPost, Subscription, UserProfile

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'account_type', 'price', 'access_level', 'is_active']
    list_filter = ['account_type', 'access_level', 'is_active']
    search_fields = ['name', 'features']
    ordering = ['price']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'is_premium_user', 'bots_setup_fee_paid']
    list_filter = ['subscription', 'is_premium_user', 'bots_setup_fee_paid']
    search_fields = ['user__username', 'user__email']
    ordering = ['user__username']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
    list_filter = ['date']
    search_fields = ['name', 'message']
    ordering = ['-date']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'bots_setup_fee', 'payment_status', 'purchase_date']
    list_filter = ['payment_status', 'subscription']
    search_fields = ['user__username', 'subscription__name']
    ordering = ['-purchase_date']

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at']
    search_fields = ['user__username', 'title', 'content']
    list_filter = ['created_at']
    ordering = ['-created_at']
