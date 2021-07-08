from django.contrib.auth import get_user_model
from django.http.response import Http404
from django.test import TransactionTestCase

from blog.forms import CommentForm, EmailPostForm, SubscribeForm
from blog.models import Post, Comment, Subscribe
from blog.services import filters_articles_by_search, makes_pagination, \
    filters_articles_by_tag, retrieves_a_tag, published_articles_list, \
    subscribe_error, retrieves_a_post, post_comments, similar_posts, \
    saves_new_comment, sends_mail, _post_tags_ids, _retrieves_similar_posts


class TestServices(TransactionTestCase):
    '''
    Тестирует сервисы
    '''
    def setUp(self):

        # Регистрируем пользователя
        User = get_user_model()
        self.user = User.objects.create(username='test_user',
                                        password='password')

        # Создаем объекты статьи
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
        self.post.tags.add('test_tag')

        self.another_post = Post.objects.create(
                        title = 'another_test_title',
                        slug = 'another_test_title',
                        author = self.user,
                        body = 'another_test_body',
                        publish = '2021-05-11 14:31:59+00',
                        created = '2021-05-11 14:31:57+00',
                        updated = '2021-05-11 14:31:58+00',
                        status = 'published',
                     )
        self.another_post.tags.add('test_tag')

        self.post_query = Post.objects.all()

    def test_published_articles_list(self):
        pub_articles = published_articles_list()
        self.assertIn(self.post, pub_articles)

    def test_retrieves_a_tag(self):
        tag = retrieves_a_tag('test_tag')
        self.assertTrue(tag)

    def test_filters_articles_by_tag(self):
        tag = retrieves_a_tag('test_tag')
        filtered_articles = filters_articles_by_tag(tag.id)
        self.assertIn(self.post, filtered_articles)

    def test_filters_articles_by_search(self):
        filtered_articles1 = filters_articles_by_search('test_body')
        filtered_articles2 = filters_articles_by_search('test_fake')
        self.assertIn(self.post, filtered_articles1)
        self.assertNotIn(self.post, filtered_articles2)

    def test_makes_pagination(self):
        pagination = makes_pagination(self.post_query, 'fake_page')
        self.assertTrue(pagination)

    def test_subscribe_error(self):
        subscribe = Subscribe.objects.create(
            subscriber_email='test@test.test')
        form = SubscribeForm(data={'subscriber_email':'test@test.test'})
        self.assertFalse(form.is_valid())
        self.assertEqual(subscribe_error(form),
            'Почта test@test.test уже зарегистрирована')

    def test_retrieves_a_post(self):
        post1 = retrieves_a_post(self.post.slug) 
        post2 = retrieves_a_post(self.post.id)
        self.assertEqual(post1, self.post)
        self.assertEqual(post2, self.post)
        
    def test_post_comments(self):
        comment = Comment.objects.create(
            post = self.post,
            name = 'Test Name',
            email = 'test@test.test',
            body = 'comment body')
        comments = post_comments(self.post)
        self.assertIn(comment, comments)

    def test__post_tags_ids(self):
        tags_ids = _post_tags_ids(self.post)
        self.assertTrue(tags_ids)

    def test__retrieves_similar_posts(self):
        tags_ids = _post_tags_ids(self.post)
        similar_posts = _retrieves_similar_posts(self.post, tags_ids)
        self.assertIn(self.another_post, similar_posts)

    def test_similar_posts(self):
        sim_posts = similar_posts(self.post)
        self.assertIn(self.another_post, sim_posts)

    def test_saves_new_comment(self):
        form = CommentForm(data={
           'name': 'Test User',
           'email': 'test@test.test',
           'body': 'test comment body'
        })
        saves_new_comment(form, self.post)
        new_comment = Comment.objects.get(body='test comment body')
        self.assertEqual(new_comment.body, 'test comment body')

    def test_sends_mail(self):
        form = EmailPostForm(data={
            'name': 'Test User',
            'email': 'test@test.test',
            'to': 'test@test.test',
            'comments': 'test comment'
        })
        post_url = '/test_url'        
        if form.is_valid():
            self.assertTrue(sends_mail(self.post, form, post_url))
        
