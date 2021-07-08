from django.test import TestCase
from blog.forms import EmailPostForm, CommentForm, SubscribeForm, SearchForm


class TestForms(TestCase):
    '''
    Тестирует формы.
    '''
    def test_email_post_form_valid_data(self):
        form = EmailPostForm(data={
           'name': 'Test User',
           'email': 'test@test.test',
           'to': 'test@test.test',
           'comment': 'test comment'
        })
        self.assertTrue(form.is_valid())

    def test_email_post_form_no_data(self):
        form = EmailPostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_comment_form_valid_data(self):
        form = CommentForm(data={
           'name': 'Test User',
           'email': 'test@test.test',
           'body': 'test comment'
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_search_form_valid_data(self):
        form = SearchForm(data={'search_query': 'search_query'})
        self.assertTrue(form.is_valid())

    def test_search_form_no_data(self):
        form = SearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_subscribe_form_valid_data(self):
        form = SubscribeForm(data={'subscriber_email': 'test@test.test'})
        self.assertTrue(form.is_valid())

    def test_subscribe_form_no_data(self):
        form = SubscribeForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
