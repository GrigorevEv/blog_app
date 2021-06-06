from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown

from .. forms import SubscribeForm, SearchForm, CommentForm
from .. models import Post


register = template.Library()

@register.inclusion_tag('blog/post/comment_form.html')
def comment_form(post_id):
    return {'comment_form': CommentForm(),
            'post_id': post_id}


@register.inclusion_tag('blog/post/search_form.html')
def search_form():
    return {'search_form': SearchForm()}

@register.inclusion_tag('blog/post/subscribe_form.html')
def subscribe_form():
    return {'subscribe_form': SubscribeForm()}


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments'))\
                         .order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='plural_comment')
def adds_endings_to_a_word_comment(number_of_comments: int) -> str:
    '''
    Adds endings to a word on russian language
    for a word "комментарий"
    '''
    if number_of_comments % 100 in [11, 12, 13, 14, 15, 16, 17, 18, 19] \
    or number_of_comments % 10 in [0, 5, 6, 7, 8, 9]:
        return 'ев'
    elif number_of_comments % 10 in [2, 3, 4]:
        return 'я'
    else:
        return 'й'


@register.filter(name='plural_result')
def adds_endings_to_a_word_result(number_of_results: int) -> str:
    '''
    Adds endings to a word on russian language
    for a word "результат"
    '''
    if number_of_results % 100 in [11, 12, 13, 14, 15, 16, 17, 18, 19] \
    or number_of_results % 10 in [0, 5, 6, 7, 8, 9]:
        return 'ов'
    elif number_of_results % 10 in [2, 3, 4]:
        return 'а'
    else:
        return ''

