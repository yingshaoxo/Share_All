from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.contrib.staticfiles.templatetags.staticfiles import static

from django.contrib.auth.models import User as UserAccount
from django.contrib.auth import authenticate
from django.contrib.auth import login as account_login
from django.contrib.auth import logout as account_logout

from .forms import LoginForm
from django.contrib import messages
from functools import wraps
# import requests
import os

BOOKMARKS_PATH = 'static/bookmarks'

# Create your views here.
def check_recaptcha(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': '6LcWDB4UAAAAAE2kgwBxVRAUOC6OZZqZguFd2pHD',
                'response': recaptcha_response
           }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

#@check_recaptcha
def index(request):
    context = {
        'munu': [{'name': 'Back', 'url': '..'}],
        'error': None,
        'redirect': None,
        'page_name': 'login'
        }
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():# and request.recaptcha_is_valid:
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['passwd']
            func = form.cleaned_data['btn']
            if username.count(' ') > 0 or passwd.count(' ') > 0:
                context['error'] = 'no space!'
                return render(request, 'login/index.html', context)

            if 'last_url' in request.COOKIES:
                context['redirect'] = request.COOKIES['last_url']
            else:
                context['redirect'] = '/'

            if func == 'Login':
                user = authenticate(username=username, password=passwd)
                if user is not None:
                    account_login(request, user)
                else:
                    context['error'] = 'password error.'
                    context['redirect'] = None

            elif func == 'Visit':
                if authenticate(username='Visitor', password='1234') is None:
                    user = UserAccount.objects.create_user('Visitor', '', '1234')
                    user.save()
                user = authenticate(username='Visitor', password='1234')
                account_login(request, user)

            elif func == 'Register':
                user = authenticate(username=username, password=passwd)
                if user is None:
                    user = UserAccount.objects.create_user(username, '', passwd)
                    user.save()
                    user = authenticate(username=username, password=passwd)
                    account_login(request, user)
                else:
                    context['error'] = 'this account already been used.'
                    context['redirect'] = None
        else:
            context['error'] = 'try again.'
            return render(request, 'login/index.html', context)

    return render(request, 'login/index.html', context)

