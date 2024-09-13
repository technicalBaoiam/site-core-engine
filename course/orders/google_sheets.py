import os
from decimal import Decimal
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from course.serializers import EnrollmentSerializer


def convert_decimal(value):

    return float(value) if isinstance(value, Decimal) else value

def convert_datetime(value):

    return value.isoformat() if isinstance(value, datetime) else value



def get_sheets_data():

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR / "course/orders/google_sheets_config.json")
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('sheets', 'v4', credentials=credentials)


def get_next_serial_number(sheet_id):

    service = get_sheets_data()
    range_name = 'Sheet1!A:A'
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name
    ).execute()
    values = result.get('values', [])
    return len(values) + 1


def prepare_enrollment_data(enrollment, order_id):

    return [
        enrollment.enrollment_number,
        enrollment.student.first_name,
        enrollment.student.last_name,
        enrollment.student.email,
        enrollment.course.title,
        convert_decimal(enrollment.plan.price),
        enrollment.plan.name,
        enrollment.type,
        convert_decimal(enrollment.payment_due),
        convert_datetime(enrollment.created_at),
        convert_datetime(enrollment.updated_at),
        order_id
    ]


def update_student_payment(sheet_id, enrollment_data, sr_no):

    service = get_sheets_data()
    range_name = 'Sheet1!A7'
    values = [[sr_no] + enrollment_data]
    body = {'values': values}
    result = service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption="RAW", body=body
    ).execute()
    return result


def update_enrollment_in_sheet(enrollment, order_id):

    sheet_id = '18NRcMt_3vP4qFZi9o54y7tP0dwKYX3fNdbLJZlrW0U8'
    
    try:
        sr_no = get_next_serial_number(sheet_id)
        enrollment_data = prepare_enrollment_data(enrollment, order_id)
        update_student_payment(sheet_id, enrollment_data, sr_no)
        print("Sheet updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


