from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from djoser.signals import user_registered
from django.conf import settings

from .models import Contact


@receiver(user_registered)
def send_registration_email(sender, user, **kwargs):
    subject = 'Добро пожаловать в сервис закупок розничной сети!'
    message = f'Спасибо за регистрацию {user.first_name} {user.last_name}!\nРады вас приветствовать на нашей платформе!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Contact)
def order_status_confirm(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Изменение статуса заказа',
            f'{instance.user}, cтатус вашего заказа по адресу {instance} изменен на "Новый".',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL]
        )

@receiver(post_delete, sender=Contact)
def order_status_delete(sender, instance, **kwargs):
    send_mail(
        'Изменение статуса заказа',
        f'{instance.user}, cтатус вашего заказа по адресу {instance} изменен на "Удален".',
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_FROM_EMAIL]
    )