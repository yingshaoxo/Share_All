from django.shortcuts import get_object_or_404, get_list_or_404, render

from django.contrib.auth.models import User as UserAccount
from django.contrib.auth import authenticate

from .forms import LoginForm

from .models import User
# Create your views here.
def index(request):
    user_list = User.objects.all()[:7]
    context = {
        'user_list': user_list,
        'title': [{'name': 'Share all', 'url': '/main/'}],
        'munu': [{'name': 'Upload', 'url': '#'}, {'name': 'Login', 'url': 'login'}],
        'page_name': 'home'}
    return render(request, 'main/index.html', context)

def login(request):
    context = {
        'title': [{'name': 'Share all', 'url': '/main/'}],
        'munu': [{'name': 'Upload', 'url': '#'}, {'name': 'Logout', 'url': '#'}],
        'error': None,
        'page_name': 'login'}
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['passwd']
            func = form.cleaned_data['btn']

            if func == 'Login':
                user = authenticate(username=username, password=passwd)
                if user is not None:
                    context['error'] = 'ok, you loged in'
                else:
                    context['error'] = 'password error'

            elif func == 'Visit':
                if authenticate(username='Visitor', password='1234') is None:
                    user = UserAccount.objects.create_user('Visitor', '', '1234')
                    user.save()
                authenticate(username='Visitor', password='1234')

            elif func == 'Register':
                user = UserAccount.objects.create_user(username, '', passwd)
                user.save()
                context['error'] = 'registed'               

    return render(request, 'main/index.html', context)

def detail(request, user_name):
    user = get_object_or_404(User, user_name=user_name)
    data = user.data_set.all()
    context = {
        'all_data': data,
        'title': [{'name': 'Share all', 'url': '/main/'}],
        'munu': [{'name': 'Back', 'url': '..'}],
        'page_name': 'detail'}
    return render(request, 'main/index.html', context)
