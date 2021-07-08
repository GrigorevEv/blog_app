from django.test import SimpleTestCase
from django.urls import resolve, reverse

from blog.views import published_articles, articles_by_tag, \
    articles_by_search, subscribe, post_detail, comment_form, post_share


class TestUrls(SimpleTestCase):
    '''
    Тестирует разрешения урлов во вьюшки
    '''
    def test_published_articles_resolved(self):
        url = reverse('blog:published_articles')
        self.assertEquals(resolve(url).func, published_articles)

    def test_articles_by_tag_resolved(self):
        url = reverse('blog:articles_by_tag', args=['tag_slug'])
        self.assertEquals(resolve(url).func, articles_by_tag)

    def test_articles_by_search_resolved(self):
        url = reverse('blog:articles_by_search') 
        self.assertEquals(resolve(url).func, articles_by_search)

    def test_subscribe_resolved(self):
        url = reverse('blog:subscribe') 
        self.assertEquals(resolve(url).func, subscribe)

    def test_post_detail_resolved(self):
        url = reverse('blog:post_detail', args=['article_slug']) 
        self.assertEquals(resolve(url).func, post_detail)

    def test_comment_form_resolved(self):
        url = reverse('blog:comment_form', args=[777]) 
        self.assertEquals(resolve(url).func, comment_form)

    def test_post_share_resolved(self):
        url = reverse('blog:post_share', args=[777]) 
        self.assertEquals(resolve(url).func, post_share)

