# views.py

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from course.models import Enrollment, Plan, Order
from course.serializers import OrderSerializer
from .utils import create_order_and_process_payment
from ..services.payment_service import PaymentService
from .send_order_email import send_order_confirmation_email, send_demo_session_email
from django.core.exceptions import ObjectDoesNotExist
from .google_sheets import update_enrollment_in_sheet


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(student=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        plan_id = request.data.get('plan_id')
    
        if not plan_id:
            return Response({"error": "plan_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if an order already exists for this Plan
            print('plan check')
            if Order.objects.filter(plan=plan_id, student=request.user).exists():
                return Response({"error": "An order already exists for this Plan and Student."}, status=status.HTTP_400_BAD_REQUEST)

            plan = Plan.objects.get(id=plan_id)
            print(plan, 'plan')
            total_amount = plan.price

            # utility function to create an order and process payment
            order = create_order_and_process_payment(request.user, plan, total_amount)

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        except Plan.DoesNotExist:
            return Response({"error": "Plan not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DemoSessionOrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        demo_fee = 100  # Fixed fee for demo session

        if not plan_id:
            return Response({"error": "plan_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        elif Order.objects.filter(plan=plan_id, student=request.user).exists():
                return Response({"error": "An order already exists for this Plan and Student."}, status=status.HTTP_400_BAD_REQUEST)    

        try:
            plan = Plan.objects.get(id=plan_id)
            
            # Create the order and process payment
            order = create_order_and_process_payment(request.user, plan, demo_fee)

            # Return order data
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
        except Plan.DoesNotExist:
            return Response({"error": "Plan not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
           
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    def put(self, request, *args, **kwargs):

        enrollment_id = request.data.get('enrollment_id')
        if not enrollment_id:
            return Response({"error": "enrollment_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Create the order and process payment
            enrollment = get_object_or_404(Enrollment, id=enrollment_id)
            if enrollment.payment_due == 0:
                return Response({"error": "Enrollment with this Plan already purchased"}, status=status.HTTP_400_BAD_REQUEST)

            order = create_order_and_process_payment(request.user, enrollment.plan, enrollment.payment_due)
            # Return order data
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        except Exception as e:
           
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class VerifyPaymentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        payment_id = request.data.get('payment_id')
        signature = request.data.get('signature')

        try:
            order = get_object_or_404(Order, order_id=order_id)
            payment_service = PaymentService()

            if  payment_service.verify_payment_signature(payment_id, order_id, signature):
                order.signature = signature
                order.status = 'paid'
                order.save()
                
                # Handle enrollment based on order amount
                self.handle_enrollment(order)

                # Send order confirmation and demo session email
                send_order_confirmation_email(request.user, order)
                if order.total_amount == 100:  # Assuming 100 is the demo session fee
                    send_demo_session_email(request.user, order)

                # send enrollment data in sheets    
                enrollment = Enrollment.objects.get(student=self.request.user, plan=order.plan)
                update_enrollment_in_sheet(enrollment, order.order_id)
                return Response({"message": "Payment verified successfully!"}, status=status.HTTP_200_OK)

            else:
                order.status = 'failed'
                order.save()
                return Response({"error": "Payment verification failed."}, status=status.HTTP_400_BAD_REQUEST)

        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({"error": f"An unexpected error occurred. {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     
    def handle_enrollment(self, order):
        demo_amount = 100  # Demo session price

        try:
        # Attempt to get existing enrollment
            enrollment = Enrollment.objects.get(plan=order.plan, student=self.request.user)
            print('Checking existing enrollment:', enrollment)

        # If enrollment exists and is for a demo session
            if order.total_amount == demo_amount:
            # Update payment_due and type for the existing demo session enrollment
               enrollment.payment_due = order.plan.price - demo_amount
               enrollment.type = 'demo'
               print('Checking existing enrollment if:', enrollment)

               enrollment.save()
            else:
            # Update payment_due to 0 if it's a full course enrollment
               enrollment.payment_due = 0
               enrollment.type = 'full'
               print('Checking existing enrollment else:', enrollment)

               enrollment.save()

        except ObjectDoesNotExist:
        # Create a new enrollment if it doesn't exist
            print('obj exception')
            Enrollment.objects.create(
               student=self.request.user,
               course=order.plan.course,
               plan=order.plan,
               payment_due=order.plan.price - demo_amount if order.total_amount == demo_amount else 0,
               type='demo' if order.total_amount == demo_amount else 'full'
        )   
     
  