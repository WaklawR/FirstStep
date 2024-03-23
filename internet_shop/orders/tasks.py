import smtplib

from django.core.mail import EmailMessage
from celery import shared_task

from orders.models import Order, OrderItem


@shared_task()
def send_order_email_task(order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order_id=order_id).all()
    items = "\n".join(
        [f"{item.quantity}x{item.product} = {item.get_cost()}"
         for item in order_items]
    )
    subject = f'Your Order ID {order.id}'
    message = f'{items}'
    try:
        msg = EmailMessage(
            subject,
            message,
            to=[order.email],
        )
        msg.send()
    except smtplib.SMTPRecipientsRefused as e:
        print(e)
    else:
        order.mailed = True
        order.save()


@shared_task()
def check_not_mailed_orders_task():
    orders_ids = [item.id for item in Order.objects.filter(mailed=False).all()]
    if orders_ids:
        for order_id in orders_ids:
            send_order_email_task.delay(order_id)
