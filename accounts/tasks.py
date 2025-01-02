import logging
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import CustomUser as User
from .tokens import account_activation_token

logger = logging.getLogger(__name__)

@shared_task
def send_verification_email(user_id, domain):
    try:
        user = User.objects.get(pk=user_id)
        mail_subject = 'Activate your account.'
        message = render_to_string('mail.html', {'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
         })
        
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
    except User.DoesNotExist:
        logger.error("User doesn't exist")
    except Exception as e:
        logger.exception(f'There is an error occured - ',{e})

    
