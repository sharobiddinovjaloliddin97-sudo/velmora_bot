from .models import Loyalty


class LoyaltyService:
    @staticmethod
    def get_loyalty(user):
        loyalty, _ = Loyalty.objects.get_or_create(
            user=user,
        )
        return loyalty

    @staticmethod
    def add_coin(user):
        loyalty = LoyaltyService.get_loyalty(user)

        loyalty.coins += 1
        loyalty.save()

        return loyalty

    @staticmethod
    def redeem_voucher(user):
        loyalty = LoyaltyService.get_loyalty(user)

        if loyalty.coins >= 5:
            loyalty.coins -= 5
            loyalty.vouchers += 1
            loyalty.save()

        return loyalty