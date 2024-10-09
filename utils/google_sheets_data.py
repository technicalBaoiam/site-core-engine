import os
import gspread
from datetime import datetime
from django.conf import settings
from google.oauth2.service_account import Credentials

def convert_datetime(value):

    if isinstance(value, datetime):
        return value.strftime('%B %d, %Y at %I:%M %p')
    return value

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
    # academic_sheet = client.open("Academic Team Enrollment Data").sheet1
    academic_sheet = client.open("Enrollment Form (Sales)").sheet1
    academic_sheet.append_row([
        convert_datetime(enrollment.enrollment_time),
        enrollment.student_full_name,
        enrollment.student_email,
        enrollment.student_phone,
        enrollment.course,
        # enrollment.enrollment_type,
      
    ])

    # Open the sales team enrollment sheet
    # sales_enrollment_sheet = client.open("Sales Team Enrollment Data").sheet1
    sales_enrollment_sheet = client.open("Enrollment Form (academic) (Responses)").sheet1
    sales_enrollment_sheet.append_row([
        convert_datetime(enrollment.enrollment_time),
        enrollment.student_full_name,
        enrollment.student_email,
        enrollment.student_phone,
        enrollment.course,
        # enrollment.enrollment_type,
    ])

# Function to save gcep contact info
def save_contact_info(contact):
    client = get_gspread_client()
    print('g sheets in action')
    # Open the sales team contact sheet
    # sales_contact_sheet = client.open("Sales Team GCEP Data").sheet1
    sales_contact_sheet = client.open("GCEP Form (Responses)").sheet1
    sales_contact_sheet.append_row([
        convert_datetime(contact.timestamp),
        f"{contact.first_name} {contact.last_name}",
        contact.phone,
        contact.email,
        
        # contact.institute,
        # contact.designation,
        # contact.contact_type,
        # contact.message,
    ])

# Function to save contact info
def save_contact_us_info(data):
    client = get_gspread_client()
    print('g sheets in action')
    # Open the sales team contact sheet
    contact_us_sheet = client.open("Contact Us Form (Responses)").sheet1

    source = "Contact Us" if 'message' in data else "Newsletter"

    contact_us_sheet.append_row([
        convert_datetime(data.get('timestamp')), 
        data['email'],                      
        data.get('full_name', 'N/A'),       
        data.get('phone', 'N/A'),             
        data.get('enquiry_type', 'N/A'),    
        data.get('message', 'N/A'),             
        data.get('newsletter', 'N/A'),      
        source,                        
    ])
