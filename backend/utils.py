import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_sms_notification(phone, message):
    """Send SMS notification (integrate with Twilio or similar)"""
    # This is a placeholder for SMS integration
    # In production, integrate with Twilio, AWS SNS, or similar service
    print(f"SMS to {phone}: {message}")

def send_email_notification(email, subject, body):
    """Send email notification"""
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('MAIL_USERNAME')
        msg['To'] = email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # SMTP server details
        server = smtplib.SMTP(os.getenv('MAIL_SERVER'), int(os.getenv('MAIL_PORT')))
        server.starttls()
        server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def generate_pdf_report(complaint):
    """Generate PDF report for complaint (integrate with reportlab)"""
    # This is a placeholder for PDF generation
    # In production, use reportlab or similar to generate PDFs
    return f"Report for {complaint.ref_id}"

translations = {
    'en': {
        'complaint_registered': 'Your grievance has been registered',
        'ref_id': 'Reference ID',
        'status': 'Status',
        'category': 'Category',
        'priority': 'Priority'
    },
    'hi': {
        'complaint_registered': 'आपकी शिकायत दर्ज की गई है',
        'ref_id': 'संदर्भ आईडी',
        'status': 'स्थिति',
        'category': 'श्रेणी',
        'priority': 'प्राथमिकता'
    }
}

def get_translated_message(key, language='en'):
    """Get translated message"""
    lang = language.lower()[:2]
    if lang not in translations:
        lang = 'en'
    return translations[lang].get(key, translations['en'].get(key, ''))
