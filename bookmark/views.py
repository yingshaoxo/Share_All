from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.contrib.staticfiles.templatetags.staticfiles import static

from django.contrib.auth.models import User as UserAccount
from django.contrib.auth import authenticate
from django.contrib.auth import login as account_login
from django.contrib.auth import logout as account_logout

from .forms import UploadFileForm
import os

BOOKMARKS_PATH = 'static/bookmarks'

# Create your views here.
def index(request): 
    real_user_list = UserAccount.objects.all().order_by('-last_login')[:7]
    user_list = [user.username for user in real_user_list]
    context = {
        'user_list': None,
        'munu': [{'name': 'Upload', 'url': 'upload'}, ],
        'redirect': None,
        'page_name': 'home'
        }
    try:
        if request.GET['func'] == 'logout':
            account_logout(request)
            context['redirect'] = '.'
    except:
        pass
    if request.user.is_authenticated:
        context['munu'].append({'name': 'Logout', 'url': '?func=logout'})
    for num, user in enumerate(real_user_list, start=0):
        if not os.path.isfile(BOOKMARKS_PATH + '/' + user.username + '.html'):
            if request.user.username == 'yingshaoxo':
                real_user_list[num].delete()
                os.remove(BOOKMARKS_PATH + '/' + real_user_list[num].username + '.html')
            del user_list[num]
    context['user_list'] = user_list
    return render(request, 'bookmark/index.html', context)

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
    return render(request, 'bookmark/index.html', context)

def upload(request):
    context = {
        'munu': [{'name': 'Back', 'url': '..'}],
        'error': None,
        'redirect': None,
        'page_name': 'upload'
        }
    if not request.user.is_authenticated:
        context['redirect'] = '/login/'
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
                path = BOOKMARKS_PATH 
                if not os.path.exists(path):
                    os.mkdir(path)
                with open(path + '/' + user.username + '.html', 'wb') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

                with open(path + '/' + user.username + '.html', 'r') as f:
                    text = f.read()
                text = text.replace('A HREF="', 'A target="_blank" HREF="')
                with open(path + '/' + user.username + '.html', 'w') as f:
                    f.write(text)

                context['redirect'] = '..'
        else:
            context['error'] = 'please try again.'

    response = render(request, 'bookmark/index.html', context)
    response.set_cookie('last_url', request.path)
    return response

