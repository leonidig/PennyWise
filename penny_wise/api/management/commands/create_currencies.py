from django.core.management.base import BaseCommand
from ...models import Currency

# python manage.py create_currencies

class Command(BaseCommand):
    help = "Create default currencies"

    def handle(self, *args, **kwargs):
        defaults = [
            {"code": "USD", "symbol": "$"},
            {"code": "EUR", "symbol": "€"},
            {"code": "UAH", "symbol": "₴"},
            {"code": "BTC", "symbol": "₿"},
        ]

        for currency in defaults:
            obj, created = Currency.objects.get_or_create(code=currency["code"], defaults={"symbol": currency["symbol"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.code}"))
            else:
                self.stdout.write(self.style.WARNING(f"Exists: {obj.code}"))
