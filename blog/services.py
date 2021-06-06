from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Page, Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from taggit.models import Tag
from typing import Optional, Union

from .models import Post
from .forms import SubscribeForm, CommentForm, EmailPostForm


def published_articles_list() -> QuerySet:
    '''
    Возвращает все опубликованные статьи.
    '''
    return Post.published.all()
 

def filters_articles_by_tag(tag: Tag) -> QuerySet:
    '''
    Возвращает QuerySet опубликованных статей, отфильтрованных
    в соответствии с выбранным тегом.
    '''
    return published_articles_list().filter(tags__in=[tag])


def filters_articles_by_search(search_query: str) -> QuerySet:
    '''
    Возвращает QuerySet опубликованных статей, отфильтрованных
    в соответствии с поисковым запросом.
    '''
    return published_articles_list().annotate(
               search=SearchVector('title', 'body'),
                ).filter(search=search_query)


def makes_pagination(object_list: QuerySet, page: Optional[str]=None) -> Page:
    '''
    Делает пагинацию страницы.
    '''
    paginator = Paginator(object_list, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def retrieves_a_tag(tag_slug: str) -> Union[Tag, Http404]:
    '''
    Возвращает объект тега из слага тега.
    В противном случае возвращает 404.
    '''
    return get_object_or_404(Tag, slug=tag_slug)


def subscribe_error(subscribe_form: SubscribeForm) -> str:
    '''
    Возвращает ошибку валидации формы в виде строки.
    Ошибки прописаны в классе SubscribeForm модуля Forms.
    '''
    return subscribe_form.errors['subscriber_email'][0]


def retrieves_a_post(post_slug_or_id: Union[str,int]) -> Union[Post, Http404]:
    '''
    Возвращает объект опубликованной статьи из слага статьи.
    В противном случае возвращает 404.
    '''
    if type(post_slug_or_id) == str:
        return get_object_or_404(Post, slug=post_slug_or_id,
                                 status='published')
    else:
        return get_object_or_404(Post, id=post_slug_or_id,
                                 status='published')


def post_comments(post: Post) -> QuerySet:
    '''
    Возвращает комментарии текущей статьи.
    '''
    return post.comments.filter(active=True).order_by('-created')


def _post_tags_ids(post: Post) -> QuerySet:
    '''
    Возвращает id тегов текущего поста.
    '''
    return post.tags.values_list('id', flat=True)


def _retrieves_similar_posts(post: Post, tags_ids: QuerySet) -> QuerySet:
    '''
    Возвращает похожие посты, сравнивая их с текущим
    по количеству одинаковых тегов.
    '''
    sim_posts = Post.published.filter(tags__in=tags_ids)\
                                  .exclude(id=post.id)
    return sim_posts.annotate(same_tags=Count('tags'))\
                             .order_by('-same_tags','-publish')[:4]


def similar_posts(post: Post) -> QuerySet:
    '''
    Возвращает похожие посты на текущий.
    '''
    return _retrieves_similar_posts(post, _post_tags_ids(post))


def saves_new_comment(comment_form: CommentForm, post):
    '''
    Присваивает комментарию объект поста и
    сохраняет комментарий в базу.
    '''
    new_comment = comment_form.save(commit=False)
    new_comment.post = post
    new_comment.save()


def sends_mail(post: Post, form: EmailPostForm, post_url) -> bool:
    '''
    Извлекает данные из формы и отсылает почту.
    '''
    cd = form.cleaned_data
    subject = F"{cd['name']}({cd['email']}) " \
              F"рекомендует вам \"{post.title}\""
    message = F"Почитать статью \"{post.title}\" можно по ссылке {post_url}\n\n" \
              F"{cd['name']}, комментарий : {cd['comments']}"
    send_mail(subject, message, 'tmail4545@gmail.com', [cd['to']])
    return True

