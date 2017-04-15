from django.shortcuts import get_object_or_404, get_list_or_404, render

from django.contrib.auth.models import User as UserAccount
from django.contrib.auth import authenticate
from django.contrib.auth import login as account_login
from django.contrib.auth import logout as account_logout

from .forms import LoginForm, UploadFileForm
import os

# Create your views here.
def index(request): 
    user_list = UserAccount.objects.all().order_by('-id')[:7]
    context = {
        'user_list': user_list,
        'munu': [{'name': 'Upload', 'url': 'upload'}, ],
        'redirect': None,
        'page_name': 'home'
        }
    try:
        if request.GET['func'] == 'logout':
            account_logout(request)
            context['redirect'] = '.'
    except:
        print('')
    if request.user.is_authenticated:
        context['munu'].append({'name': 'Logout', 'url': '?func=logout'})
        if request.user.username == 'yingshaoxo':
            for num, user in enumerate(user_list, start=0):
                if not os.path.isfile('Shared_Page' + '/' + user.username + '.html'):
                    user_list[num].delete()
    return render(request, 'main/index.html', context)

def detail(request, user_name):
    user = get_object_or_404(UserAccount, username=user_name)
    try:
        data = user.data_set.all()
    except:
        data = None
    context = {
        'all_data': data,
        'munu': [{'name': 'Back', 'url': '..'}],
        'page_name': 'detail'
        }
    return render(request, 'main/index.html', context)

def upload(request):
    context = {
        'munu': [{'name': 'Back', 'url': '..'}],
        'error': None,
        'redirect': None,
        'page_name': 'upload'
        }
    if not request.user.is_authenticated:
        context['page_name'] = 'login'
    else:
        context['page_name'] = 'upload'
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(UserAccount, username=request.user.username)
            f = request.FILES['file'] 
            if f._size > 5242880 or 'text/html' != f.content_type:
                context['error'] = 'this file too big or we only support html.'
            else:
                path = 'Shared_Page' 
                if not os.path.exists(path):
                    os.mkdir(path)
                with open(path + '/' + user.username + '.html', 'wb') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

                '''with open(path + '/' + user.username + '.html', 'r') as f:
                    text = f.read()
                text = text.replace('A HREF="', 'A target="_blank" HREF="')
                with open(path + '/' + user.username + '.html', 'w') as f:
                    f.write(text)'''

                context['redirect'] = '..'
        else:
            context['error'] = 'please try again.'

    return render(request, 'main/index.html', context)

def login(request):
    context = {
        'munu': [{'name': 'Back', 'url': '..'}],
        'error': None,
        'redirect': None,
        'page_name': 'login'
        }
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['passwd']
            func = form.cleaned_data['btn']
            if username.count(' ') > 0 or passwd.count(' ') > 0:
                context['error'] = 'no space!'
                return render(request, 'main/index.html', context)

            if func == 'Login':
                user = authenticate(username=username, password=passwd)
                if user is not None:
                    context['redirect'] = '../upload/'
                else:
                    context['error'] = 'password error.'

            elif func == 'Visit':
                if authenticate(username='Visitor', password='1234') is None:
                    user = UserAccount.objects.create_user('Visitor', '', '1234')
                    user.save()
                user = authenticate(username='Visitor', password='1234')
                context['redirect'] = '../upload/'

            elif func == 'Register':
                user = authenticate(username=username, password=passwd)
                if user is None:
                    user = UserAccount.objects.create_user(username, '', passwd)
                    user.save()
                    user = authenticate(username=username, password=passwd)
                    context['redirect'] = '../upload/'
                else:
                    context['error'] = 'this account already been used.'
        else:
            context['error'] = 'try again.'
            return render(request, 'main/index.html', context)
    account_login(request, user)
    return render(request, 'main/index.html', context)

