# Generated by Django 3.2 on 2021-05-21 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_main_page_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber_email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subscription_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')),
            ],
        ),
    ]
