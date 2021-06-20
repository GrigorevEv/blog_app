from django.contrib.auth.models import User 
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone 

from taggit.managers import TaggableManager
from .tasks import sends_mails_to_subscribers


class PublishedManager(models.Manager): 
    '''
    Менеджер для возврата всех опубликованных статей.
    '''
    def get_queryset(self): 
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')


class Post(models.Model): 
    '''
    Модель статей блога.
    '''
    STATUS_CHOICES = ( 
        ('draft', 'Черновик'), 
        ('published', 'Опубликовано'), 
    )
    title = models.CharField('Заголовок', max_length=250) 
    slug = models.SlugField('Слаг', max_length=250,
                            unique_for_date='publish') 
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField('Текст статьи') 
    publish = models.DateTimeField('Опубликовано', default=timezone.now) 
    created = models.DateTimeField('Создано', auto_now_add=True) 
    updated = models.DateTimeField('Обновлено', auto_now=True) 
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, 
                                                       default='draft')
    main_page_photo = models.ImageField('Фото на главной странице',
                                        upload_to='main_page_photos/%Y/%m/%d/',
                                        default='') 
    objects = models.Manager() 
    published = PublishedManager()
    tags = TaggableManager()

    class Meta: 
        ordering = ('-publish',) 
        verbose_name = 'пост'
        verbose_name_plural = 'Посты'

    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        '''
        Переопределяет стандартную функцию save.
        После сохранения опубликованной статьи - делает рассылку
        по почте подписчикам.
        '''
        super().save(*args, **kwargs)

        subscribers = Subscribe.objects.all()
        all_emails = []
        for subscriber in subscribers:
            all_emails.append(subscriber.subscriber_email)

        post_url = self.get_absolute_url()

        sends_mails_to_subscribers.delay(all_emails, post_url)

        
class Comment(models.Model): 
    '''
    Модель данных для комментариев статей.
    '''
    post = models.ForeignKey(Post, verbose_name='Пост',
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField('Имя', max_length=80) 
    email = models.EmailField('Email') 
    body = models.TextField('Текст комментария') 
    created = models.DateTimeField('Создан', auto_now_add=True) 
    updated = models.DateTimeField('Обновлен', auto_now=True) 
    active = models.BooleanField('Активен', default=True) 
 
    class Meta: 
        ordering = ('created',) 
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post)


class Subscribe(models.Model):
    '''
    Модель для хранения данных подписчиков
    '''
    subscriber_email = models.EmailField('Email', max_length=50, unique=True)
    subscription_date = models.DateTimeField('Дата подписки',
                                             auto_now_add=True)

    class Meta:
        ordering = ('subscription_date',)
        verbose_name = 'данные подписчиков'
        verbose_name_plural = 'данные подписчиков'

    def __str__(self):
        return self.subscriber_email
