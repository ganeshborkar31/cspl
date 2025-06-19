from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
import os
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser,ExpireToken

# def send_email(email, otp):
#     subject = 'Email Verification OTP'
#     from_email = settings.DEFAULT_FROM_EMAIL
#     recipient_list = [email]

#     context = {'otp': otp}
#     html_content = render_to_string('otp_email_template.html', context = context)

#     text_content = f'Your OTP is {otp}.'

#     msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
#     msg.attach_alternative(html_content, "text/html")

#     logo_path = os.path.join(settings.MEDIA_ROOT, 'logo.png') 
    
#     with open(logo_path, 'rb') as f:
#         image = MIMEImage(f.read())
#         image.add_header('Content-ID', '<logo_image>')
#         image.add_header('Content-Disposition', 'inline', filename='logo.png')
#         msg.attach(image)

#     msg.send()

def send_email(email, otp):
    logo_url = f'http://127.0.0.1:8000{settings.MEDIA_URL}logo.png'

    subject = 'Email Verification OTP'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email]

    context = {
        'otp': otp,
        'logo_url': logo_url,
    }

    html_content = render_to_string('email_with_logo_url.html', context)

    emailmassage = EmailMessage(subject, html_content, from_email, to_email)
    emailmassage.content_subtype = "html"  
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'resume.pdf')
    emailmassage.attach_file(pdf_path)
    emailmassage.send()
    
def threaded_send_email(email, otp):
    send_email(email, otp)

def is_user_exist(email):
    registered_mail = CustomUser.objects.filter(email = email)
    
    return registered_mail.exists()
        
        
class ExpireTokenAuthentication(TokenAuthentication):
    model = ExpireToken
    
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if token.is_expire():
            raise AuthenticationFailed('Token has expired')
        return user, token
    
def parse_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ["true", "1", "yes", "=true()"]
    if isinstance(value, str):
        return value.strip().lower() in ["false", "0", "no", "=false()"]
    return value

def sanitize_string(value):
    if value:
        return str(value).strip()
    else :
        return  ''

def sanitize_price(value):
    try:
        return float(value)
    except:
        return None
    
def sanitize_tag(tag):
    if tag in ("Veg", "VEG", "veg"):
        return str('VEG')
    
    elif tag in ("Non-Veg", "Non Veg", "non-veg", 'NON-VEG'):
        return str('NON-VEG')
    
    else :
        return None