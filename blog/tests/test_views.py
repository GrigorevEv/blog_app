from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse

from blog.forms import SubscribeForm
from blog.models import Post, Comment, Subscribe



class ViewsTest(TestCase):
    '''
    Тестирует вьюшки.
    '''
    def setUp(self):

        # Создаем клиента
        self.client = Client()

        # Регистрируем пользователя
        User = get_user_model()
        self.user = User.objects.create(username='test_user',
                                        password='password')

        # Создаем объект статьи
        self.post = Post.objects.create(
                        title = 'test_title',
                        slug = 'test_title',
                        author = self.user,
                        body = 'test_body',
                        publish = '2021-05-11 14:31:59+00',
                        created = '2021-05-11 14:31:57+00',
                        updated = '2021-05-11 14:31:58+00',
                        status = 'published',
                     )
        self.post.tags.add('body')

        # Создаем урлы к которым привязаны вьюшки
        self.published_articles_url = reverse('blog:published_articles')
        self.articles_by_tag_url = reverse('blog:articles_by_tag',
                                           args=['body'])
        self.articles_by_search_url = reverse('blog:articles_by_search')
        self.subscribe_url = reverse('blog:subscribe')
        self.post_detail_url = reverse('blog:post_detail', 
                                       args=[self.post.slug])
        self.comment_form_url = reverse('blog:comment_form',
                                        args=[self.post.id])
        self.post_share_url = reverse('blog:post_share', args=[self.post.id])


    def test_published_articles(self):
        response = self.client.get(self.published_articles_url)     
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/list.html')   

    def test_articles_by_tag(self):
        response = self.client.get(self.articles_by_tag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/list.html')   

    def test_articles_by_search(self):
        response = self.client.get(self.articles_by_search_url,
                                   {'search_query': 'body'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/list.html')   
        self.assertIn(self.post, response.context['filtered_articles'])

    def test_subscribe_post(self):
        response = self.client.post(self.subscribe_url,
                                    {'subscriber_email':'test@test.test'})
        test_subscriber = Subscribe.objects.get(
            subscriber_email='test@test.test')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_subscriber.subscriber_email, 'test@test.test')
        
    def test_subscribe_get(self):
        response = self.client.get(self.subscribe_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/subscribe_form.html')   

    def test_post_detail(self):
        response = self.client.get(self.post_detail_url)     
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/detail.html')   
        self.assertIn(self.post.body, response.content.decode('utf-8'))

    def test_comment_form_post(self):
        self.comment_form_data = dict(id=1,
                                      post = self.post.id,
                                      name = 'test_name',
                                      email = 'test_email@test.email',
                                      body = 'test_comment_body',
                                      active = True)
        response = self.client.post(self.comment_form_url,
                                    self.comment_form_data)
        test_comment = Comment.objects.get(body = 'test_comment_body')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(model_to_dict(test_comment), self.comment_form_data)

    def test_comment_form_get(self):
        response = self.client.get(self.comment_form_url)
        self.assertEqual(response.status_code, 302)

    def test_post_share_post(self):
        self.post_share_data = dict(name='test_user',
                                    email='tmail4455@gmail.com',
                                    to='tmail4455@gmail.com',
                                    comments='test_comment')
        response = self.client.post(self.post_share_url, self.post_share_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/share.html')   

    def test_post_share_get(self):
        response = self.client.post(self.post_share_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/share.html')   
