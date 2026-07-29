import os
import json
import urllib.request
from datetime import date
from django.core.management.base import BaseCommand
from apps.users.models import User
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Gives 50,000 UZS loyalty coins to users on their birthday'

    def handle(self, *args, **options):
        # Load env variables (assuming .env is at the root d:\velmora_bot)
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), '.env')
        load_dotenv(env_path)
        BOT_TOKEN = os.getenv("BOT_TOKEN")

        today = date.today()
        # Find users whose birthday is today
        birthday_users = User.objects.filter(
            date_of_birth__month=today.month,
            date_of_birth__day=today.day
        )

        if not birthday_users.exists():
            self.stdout.write(self.style.SUCCESS('No users have a birthday today.'))
            return

        for user in birthday_users:
            user.loyalty_coins += 50000
            user.save(update_fields=['loyalty_coins'])

            if not user.telegram_id or not BOT_TOKEN:
                continue

            language = getattr(user, 'language', 'uz')
            
            if language == 'uz':
                message = "🎉 Tug'ilgan kuningiz bilan!\n\n🎁 Biz sizga bayram sovg'asi sifatida 50,000 coin hadya qildik! Uni xaridlaringizda ishlatishingiz mumkin."
            else:
                message = "🎉 С днем рождения!\n\n🎁 В качестве подарка мы начислили вам 50,000 coin(ов)! Вы можете использовать их при покупках."

            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": user.telegram_id,
                "text": message
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    pass
                self.stdout.write(self.style.SUCCESS(f'Sent birthday voucher to {user.email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to send telegram notification to {user.email}: {e}'))
