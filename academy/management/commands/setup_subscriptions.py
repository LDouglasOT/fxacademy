from django.core.management.base import BaseCommand
from academy.models import Subscription

class Command(BaseCommand):
    help = 'Setup default subscription types'

    def handle(self, *args, **options):
        # Clear existing subscriptions
        Subscription.objects.all().delete()
        
        # Create Free subscription
        Subscription.objects.create(
            name="Free Account",
            account_type="free",
            price=0,
            access_level="telegram",
            features="Access to Telegram community only",
            can_access_signals=False,
            can_access_bots=False,
            can_access_classes=False,
            can_access_community=True,
        )
        
        # Create Basic subscription
        Subscription.objects.create(
            name="Basic Account",
            account_type="basic",
            price=50,
            access_level="signals",
            features="Telegram access + Trading signals",
            can_access_signals=True,
            can_access_bots=False,
            can_access_classes=False,
            can_access_community=True,
        )
        
        # Create Standard subscription
        Subscription.objects.create(
            name="Standard Account",
            account_type="standard",
            price=100,
            access_level="bots",
            features="Telegram access + Trading signals + Bots access",
            can_access_signals=True,
            can_access_bots=True,
            can_access_classes=False,
            can_access_community=True,
        )
        
        # Create Premium subscription
        Subscription.objects.create(
            name="Premium Account",
            account_type="premium",
            price=500,
            access_level="all",
            features="Full access to all features including classes",
            can_access_signals=True,
            can_access_bots=True,
            can_access_classes=True,
            can_access_community=True,
        )
        
        # Create Bots subscription (free with setup fee)
        Subscription.objects.create(
            name="Bots Account",
            account_type="bots",
            price=0,  # Free but has setup fee logic
            access_level="bots",
            features="Free bots access with $100 setup fee",
            can_access_signals=False,
            can_access_bots=True,
            can_access_classes=False,
            can_access_community=True,
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully created subscription types'))