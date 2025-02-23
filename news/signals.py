from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import PostCategory


# реализация отправки сообщений

def send_notifications(preview, pk, title, subscribers):
    html_contect = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_contect, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=PostCategory) # m2m_changed событие присваиваемой категории какой-то статье
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add': # если action это событие создание статьи post_add, то тогда мы будем отправлять пользователю уведомление
        categories = instance.category.all() # обращаемся ко всем категориям
        subscribers_emails = [] # здесь будут сохраняться все подписчики

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)