import os
from celery import Celery


# Устанавливаем переменную окружения настроек, чтобы celery их видел
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_app.settings')

# Создаем экземпляр класса Celery в качестве "приложения"
app = Celery('blog_app')

# Загружаем конфигурацию из файла настроек джанго.
# Загружаемые настройки будут начинаться с CELERY_
app.config_from_object('django.conf:settings', namespace = 'CELERY')

# Загружаем модули tasks.py из всех зарегистрированных приложений django
app.autodiscover_tasks()

