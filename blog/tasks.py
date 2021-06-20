from celery import shared_task
from django.contrib.sites.models import Site
from django.core.mail import send_mail


@shared_task
def sends_mails_to_subscribers(subscribers_emails: list, post_url: str):
    '''
    Отправляет рассылку подписчикам с информацией
    о новой статье.
    '''
    for i in range(len(subscribers_emails)):
        send_mail(
            'Муж-лягуж и Прикотятор',
            'Вышла новая интересная статья!!!\n'
            'Взгляните, она правда интересная =)\n'
            F'http://{Site.objects.get_current().domain}{post_url}',
            'tmail4545@gmail.com',
            [subscribers_emails[i]])

