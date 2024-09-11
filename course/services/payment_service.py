import razorpay
from django.conf import settings

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class PaymentService:
    def create_payment(self, total_amount):
        """Create a payment order with Razorpay."""
        try:
            payment = client.order.create({
                "amount": int(total_amount * 100),  # amount in paisa
                "currency": "INR",
                "payment_capture": 1  # Auto-capture after payment is successful
            })

            return {
                'payment_id': payment['id'],
                'order_id': payment['id'],
                'signature': ''  # Signature is handled after payment completion
            }
        except Exception as e:
            raise ValueError(f"Error creating payment: {str(e)}")

    def verify_payment_signature(self, payment_id, order_id, signature):
        """Verify the payment signature with Razorpay."""
        try:
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            client.utility.verify_payment_signature(params_dict)
            return True
        except razorpay.errors.SignatureVerificationError:
            return False
