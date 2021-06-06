from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Subscribe


class EmailPostForm(forms.Form):
    '''
    Форма для того, чтобы поделиться статьей по email
    '''
    name = forms.CharField(label='', max_length=25)
    email = forms.EmailField(label='')
    to = forms.EmailField(label='')
    comments = forms.CharField(label='', required=False, widget=forms.Textarea)
    def __init__(self, *args, **kwargs):
        super(EmailPostForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
                         {'class': 'form-name',
                          'placeholder': 'Ваше имя*'})
        self.fields['email'].widget.attrs.update(
                         {'class': 'form-email',
                          'placeholder': 'Ваш email*'})
        self.fields['to'].widget.attrs.update(
                         {'class': 'form-email',
                          'placeholder': 'Email получателя*'})
        self.fields['comments'].widget.attrs.update(
                         {'class': 'form-text',
                          'placeholder': 'Текст комментария'})


class CommentForm(forms.ModelForm):
    '''
    Форма комментариев статей
    '''
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {
            'name': '',
            'email': '',
            'body': '',
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
                         {'class': 'form-name',
                          'placeholder': 'Имя*'})
        self.fields['email'].widget.attrs.update(
                         {'class': 'form-email',
                          'placeholder': 'Email*'})
        self.fields['body'].widget.attrs.update(
                         {'class': 'form-text',
                          'placeholder': 'Текст комментария*'})
        

class SearchForm(forms.Form):
    '''
    Форма поиска статей на сайте
    '''
    search_query = forms.CharField(label='')
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search_query'].widget.attrs.update(
                         {'class': 'search-input',
                          'placeholder': 'Искать на сайте'})
    

class SubscribeForm(forms.ModelForm):
    '''
    Форма подписки на новые статьи
    '''
    class Meta:
        model = Subscribe
        fields = ('subscriber_email',)
        widgets = {
            'subscriber_email': forms.EmailInput(attrs={
                                    'class': 'subscribe-input',
                                    'placeholder': 'Введите e-mail'})
            }

        labels = {
            'subscriber_email': ''
            }
    
    def clean_subscriber_email(self):
        '''
        Функция переопределения стандартной cleaned_data с целью
        добавления валидации. В данном случае на уникальность.
        '''
        new_subscriber_email = self.cleaned_data['subscriber_email']
        if Subscribe.objects.filter(
            subscriber_email__iexact=new_subscriber_email).count():
            raise ValidationError('Почта {} уже зарегистрирована'.format(
                                        new_subscriber_email))
        return new_subscriber_email
        
