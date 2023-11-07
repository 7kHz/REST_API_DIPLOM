from django.core.mail import send_mail
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from djoser.signals import user_registered
from django.conf import settings
from django.contrib import admin

from .models import Contact, Order


@receiver(user_registered)
def send_registration_email(sender, user, **kwargs):
    subject = 'Добро пожаловать в сервис закупок розничной сети!'
    message = f'Спасибо за регистрацию {user.first_name} {user.last_name}!\nРады вас приветствовать на нашей платформе!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Contact)
def order_status_confirm(sender, instance, created, **kwargs):
    supplier = Order.objects.filter(user_id=instance.user.id). \
        select_related('product_info__product__category__shops__shop'). \
        values(email=F('product_info__product__category__shops__user__email')).distinct()
    order_number = Order.objects.filter(user_id=instance.user.id, status='New'). \
        annotate().values('order_number').distinct()
    if created:
        send_mail(
            f'Изменение статуса заказа #{order_number[0]["order_number"]}',
            f'{instance.user}, cтатус вашего заказа #{order_number[0]["order_number"]} изменен на "Новый".',
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email]
        ),
        send_mail(
            f'Получен новый заказ #{order_number[0]["order_number"]}',
            f'С деталями заказа #{order_number[0]["order_number"]} ознакомьтесь в разделе "Заказы"',
            settings.DEFAULT_FROM_EMAIL,
            [s['email'] for s in supplier]
        )


# @receiver(post_save, sender=admin)
# def admin_status_edit(sender, instance, created, **kwargs):
#     if created:
#         send_mail(
#             f'Изменение статуса заказа',
#             f'{instance.user}, cтатус вашего заказа изменен на "Новый".',
#             settings.DEFAULT_FROM_EMAIL,
#             [instance.user.email]
#         )


@receiver(post_delete, sender=Contact)
def order_status_delete(sender, instance, **kwargs):
    supplier = Order.objects.filter(user_id=instance.user.id). \
        select_related('product_info__product__category__shops__shop'). \
        values(email=F('product_info__product__category__shops__user__email')).distinct()
    order_number = Order.objects.filter(user_id=instance.user.id, status='New'). \
        annotate().values('order_number').distinct()
    send_mail(
        f'Изменение статуса заказа #{order_number[0]["order_number"]}',
        f'{instance.user}, cтатус вашего заказа #{order_number[0]["order_number"]} изменен на "Удален".',
        settings.DEFAULT_FROM_EMAIL,
        [instance.user.email]
    ),
    send_mail(
        f'Изменение статуса заказа #{order_number[0]["order_number"]}',
        f'{instance.user}, cтатус заказа #{order_number[0]["order_number"]} изменен на "Удален".',
        settings.DEFAULT_FROM_EMAIL,
        [s['email'] for s in supplier]
    )
