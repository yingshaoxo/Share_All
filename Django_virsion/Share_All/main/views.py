from django.shortcuts import get_object_or_404, get_list_or_404, render

from django.contrib.auth.models import User as UserAccount
from django.contrib.auth import authenticate
from django.contrib.auth import login as account_login
from django.contrib.auth import logout as account_logout

from .forms import LoginForm

# Create your views here.
def index(request): 
    user_list = UserAccount.objects.all()[:7]
    context = {
        'user_list': user_list,
        'munu': [{'name': 'Upload', 'url': '#'}, {'name': 'Manage', 'url': 'manage'}],
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

def manage(request):
    context = {
        'munu': [{'name': 'Back', 'url': '..'}],
        'page_name': ''
        }
    if not request.user.is_authenticated:
        context['page_name'] = 'login'
        return render(request, 'main/index.html', context)
    else:
        context['page_name'] = 'manage'
        user = get_object_or_404(UserAccount, username=request.user.username)
        try:
            data = user.data_set.all()
        except:
            data = None
        context.update({'all_data': data})
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

            if func == 'Login':
                user = authenticate(username=username, password=passwd)
                if user is not None:
                    context['redirect'] = '../manage/'
                else:
                    context['error'] = 'password error'

            elif func == 'Visit':
                if authenticate(username='Visitor', password='1234') is None:
                    user = UserAccount.objects.create_user('Visitor', '', '1234')
                    user.save()
                user = authenticate(username='Visitor', password='1234')
                context['redirect'] = '../manage/'

            elif func == 'Register':
                user = UserAccount.objects.create_user(username, '', passwd)
                user.save()
                context['error'] = 'registed'
                user = authenticate(username=username, password=passwd)
                context['redirect'] = '../manage/'

    account_login(request, user)
    return render(request, 'main/index.html', context)

