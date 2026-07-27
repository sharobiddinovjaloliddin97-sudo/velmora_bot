from .models import Payment


class PaymentService:
    @staticmethod
    def create_payment(order, payment_method):
        return Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=order.total_price,
        )

    @staticmethod
    def get_payment(order):
        return Payment.objects.get(order=order)

    @staticmethod
    def update_payment_status(
        payment,
        status,
        transaction_id=None,
    ):
        payment.status = status

        if transaction_id:
            payment.transaction_id = transaction_id

        payment.save()

        return payment