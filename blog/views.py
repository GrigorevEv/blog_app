from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CommentForm, EmailPostForm, SearchForm, SubscribeForm
from .services import filters_articles_by_search, makes_pagination, \
    filters_articles_by_tag, retrieves_a_tag, published_articles_list, \
    subscribe_error, retrieves_a_post, post_comments, similar_posts, \
    saves_new_comment, sends_mail


def published_articles(request):
    '''
    Выводит все опубликованные статьи на главной странице сайта с
    использованием пагинации.
    '''
    page=request.GET.get('page')
    posts = makes_pagination(published_articles_list(), page)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts})
                   

def articles_by_tag(request, tag_slug):
    '''
    Выводит список статей в соответствии с выбранным тегом c 
    использованием пагинации
    '''
    tag = retrieves_a_tag(tag_slug)
    filtered_articles = filters_articles_by_tag(tag)
    page=request.GET.get('page')
    posts = makes_pagination(filtered_articles, page)
    return render(request, 'blog/post/list.html',
                     {'filtered_articles': filtered_articles,
                      'page': page,
                      'posts': posts,
                      'tag': tag
                     })
     

def articles_by_search(request):
    '''
    Выводит список статей в соответствии с поисковым запросом с
    использованием пагинации
    '''
    if 'search_query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid:
            search_query = search_form.data['search_query']
            filtered_articles = filters_articles_by_search(search_query)
            page=request.GET.get('page')
            posts = makes_pagination(filtered_articles, page)
            return render(request, 'blog/post/list.html',
                             {'filtered_articles': filtered_articles,
                              'page': page,
                              'posts': posts,
                              'search_query': search_query
                         })
    return redirect('blog:published_articles')


def subscribe(request):
    '''
    Обработчик формы подписки. Включает в себя сообщение об удачной подписке и 
    сообщения ошибок валидации, указанных в классе SubscribeForm (в данном
    случае только на уникальность).
    '''
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe = subscribe_form.save()
            messages.add_message(request, messages.INFO,
                'Вы подписались на рассылку')
            return redirect('blog:published_articles')
        else:
            messages.add_message(request, messages.INFO,
                                 subscribe_error(subscribe_form))
            return redirect('blog:published_articles')
    else:
        subscribe_form = SubscribeForm()
    return render(request, 'blog/post/subscribe_form.html',
                    {'subscribe_form': subscribe_form})


def post_detail(request, post_slug):
    '''
    Отображает выбранную статью полностью, а также список похожих
    статей, комментарии, и форму комментариев.
    Последняя отображается через inclusion_tag в шаблоне detail.html.
    '''
    post=retrieves_a_post(post_slug)
    sim_posts = similar_posts(post)
    post_comm = post_comments(post)
    return render(request, 'blog/post/detail.html',
                     {'post':post,
                      'similar_posts': sim_posts,
                      'comments': post_comm
                 })


def comment_form(request, post_id):
    '''
    Обработчик формы комментариев.
    '''
    post=retrieves_a_post(post_id)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            saves_new_comment(comment_form, post)
    else:
        comment_form = CommentForm()
    return redirect('blog:post_detail', post.slug)


def post_share(request, post_id):
    '''
    Обработчик формы, которая позволяет поделиться статьей по email.
    '''
    post = retrieves_a_post(post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            post_url = request.build_absolute_uri(post.get_absolute_url())
            sent = sends_mail(post, form, post_url)
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                     {'post': post,
                     'form': form,
                     'sent': sent
                 })

