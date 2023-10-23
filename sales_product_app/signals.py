from django.core.mail import send_mail
from django.dispatch import receiver
from djoser.signals import user_registered
from django.conf import settings


@receiver(user_registered)
def send_registration_email(sender, user, **kwargs):
    subject = 'Добро пожаловать в сервис закупок розничной сети!'
    message = f'Спасибо за регистрацию {user.first_name} {user.last_name}!\nРады вас приветствовать на нашей платформе!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)