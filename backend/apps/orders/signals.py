import os
import json
import urllib.request
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order
from dotenv import load_dotenv

# Load env variables (assuming .env is at the root d:\velmora_bot)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
load_dotenv(env_path)
BOT_TOKEN = os.getenv("BOT_TOKEN")

@receiver(pre_save, sender=Order)
def capture_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Order)
def notify_order_status_change(sender, instance, created, **kwargs):
    if created:
        return
        
    old_status = getattr(instance, '_old_status', None)
    
    if old_status and old_status != instance.status:
        user = instance.user
        if not user.telegram_id:
            return
            
        language = getattr(user, 'language', 'uz')
        
        status_translations = {
            'pending': {'uz': 'Kutilmoqda ⏳', 'ru': 'В ожидании ⏳'},
            'confirmed': {'uz': 'Tasdiqlandi ✅', 'ru': 'Подтвержден ✅'},
            'shipped': {'uz': 'Yetkazib berishga berildi 🚚', 'ru': 'Отправлен 🚚'},
            'delivered': {'uz': 'Yetkazib berildi 🎉', 'ru': 'Доставлен 🎉'},
            'cancelled': {'uz': 'Bekor qilindi ❌', 'ru': 'Отменен ❌'},
        }
        
        status_text = status_translations.get(instance.status, {}).get(language, instance.status)
        
        if language == 'uz':
            message = f"🔔 Buyurtma #{instance.id} holati o'zgardi!\n\n📊 Yangi holat: {status_text}"
        else:
            message = f"🔔 Статус заказа #{instance.id} изменился!\n\n📊 Новый статус: {status_text}"

        # Grant Loyalty Coins if delivered
        if instance.status == 'delivered':
            earned_coins = int(float(instance.total_price) * 0.05) # 5% cashback
            if earned_coins > 0:
                user.loyalty_coins += earned_coins
                user.save(update_fields=['loyalty_coins'])
                if language == 'uz':
                    message += f"\n\n🎁 Tabriklaymiz! Siz ushbu buyurtmadan {earned_coins} coin ishlab topdingiz."
                else:
                    message += f"\n\n🎁 Поздравляем! Вы заработали {earned_coins} coin(ов) за этот заказ."
            
        if BOT_TOKEN:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": user.telegram_id,
                "text": message
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=5) as response:
                    pass
            except Exception as e:
                print(f"Failed to send telegram notification: {e}")
