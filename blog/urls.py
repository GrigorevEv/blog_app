from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from .feeds import LatestPostsFeed
from . import views 


app_name = 'blog'
urlpatterns = [
    path('',
         views.published_articles,
         name='published_articles'),

    path('tag/<slug:tag_slug>/',
         views.articles_by_tag,
         name='articles_by_tag'),

    path('search/', 
         views.articles_by_search,
         name='articles_by_search'),

    path('subscribe',
         views.subscribe,
         name='subscribe'),

    path('<slug:post_slug>/',
         views.post_detail,
         name='post_detail'),

    path('comment_form/<int:post_id>/',
         views.comment_form,
         name='comment_form'),

    path('<int:post_id>/share/',
         views.post_share,
         name='post_share'),

    path('feed/',
         LatestPostsFeed(),
         name='post_feed'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

