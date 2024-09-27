import os
import gspread
from datetime import datetime
from django.conf import settings
from google.oauth2.service_account import Credentials

def convert_datetime(value):

    return value.isoformat() if isinstance(value, datetime) else value

# Set up Google Sheets credentials
def get_gspread_client():
    # Load your service account credentials
    print('gsheet in action get spread')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
    SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR / "course/orders/google_sheets_config.json")
    print('gsheet in action get spread passed path')

    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    print('taken cred')
    client = gspread.authorize(creds)
    print('cred success')
    return client

# Function to save enrollment data
def save_enrollment_data(enrollment):
    client = get_gspread_client()
    print('take data in sheet')
    # Open the academic team enrollment sheet
    academic_sheet = client.open("Academic Team Enrollment Data").sheet1
    academic_sheet.append_row([
        enrollment.student_full_name,
        enrollment.student_email,
        enrollment.course,
        enrollment.student_phone,
        enrollment.enrollment_type,
        convert_datetime(enrollment.enrollment_time),
      
    ])

    # Open the sales team enrollment sheet
    sales_enrollment_sheet = client.open("Sales Team Enrollment Data").sheet1
    sales_enrollment_sheet.append_row([
        enrollment.student_full_name,
        enrollment.student_email,
        enrollment.course,
        enrollment.student_phone,
        enrollment.enrollment_type,
        convert_datetime(enrollment.enrollment_time),
    ])

# Function to save contact info
def save_contact_info(contact):
    client = get_gspread_client()
    print('g sheets in action')
    # Open the sales team contact sheet
    sales_contact_sheet = client.open("Sales Team Contact Data").sheet1
    sales_contact_sheet.append_row([
        contact.first_name,
        contact.last_name,
        contact.institute,
        contact.employer,
        contact.designation,
        contact.email,
        contact.phone,
        contact.job_title,
        contact.contact_type,
        contact.message,
    ])
