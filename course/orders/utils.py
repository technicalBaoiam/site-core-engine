# utils.py

from course.models import Order
from ..services.payment_service import PaymentService

def create_order_and_process_payment(student, plan, total_amount):
    """
    Creates an order and processes the payment.
    """
    # Create the order instance
    print('check unique constraint')
    order = Order.objects.create(
        student=student,
        plan=plan,
        total_amount=total_amount,
        status='pending'
    )
    print('check unique constraint passed')

    # Process payment
    payment_service = PaymentService()
    payment_data = payment_service.create_payment(total_amount)

    # Update order with payment details
    order.payment_id = payment_data['payment_id']
    order.order_id = payment_data['order_id']
    order.signature = payment_data['signature']
    order.save()

    return order


