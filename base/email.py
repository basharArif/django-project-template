import os
import threading

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()


class EmailThread(threading.Thread):
    def __init__(self, msg):
        self.msg = msg
        threading.Thread.__init__(self)

    def run(self):
        self.msg.send()


def send_email(subject, to, data, template):
    html_content = render_to_string(template, data)
    text_content = strip_tags(html_content)
    from_email = os.getenv('EMAIL_HOST_USER')
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    EmailThread(msg).start()


def send_account_verify_email(email, data):
    send_email(_("Please Verify Your Account"), email, data, "accounts/account_verification_email.html")


def send_password_reset_email(email, data):
    send_email(_("Password Reset Request"), email, data, 'accounts/password_reset_email.txt')
