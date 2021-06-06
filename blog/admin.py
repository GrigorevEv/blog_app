from django import forms
from django.contrib import admin

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Comment, Post, Subscribe


class PostAdminForm(forms.ModelForm):
    '''
    Создает форму с использованием редактора CKEditor 
    '''
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''
    Кастомизирует область администрирования постов
    '''
    form = PostAdminForm
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''
    Кастомизирует область администрирования комментариев
    '''
    list_display = ('name', 'post', 'email', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    '''
    Кастомизирует область администрирования подписок
    '''
    list_display = ('subscriber_email', 'subscription_date')
