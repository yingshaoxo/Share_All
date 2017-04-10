from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import User
# Create your views here.
def index(request):
    user_list = User.objects.all()[:7]
    context = {
        'user_list': user_list,
        'title': [{'name': 'Share all', 'url': '/main/'}],
        'munu': [{'name': 'Upload', 'url': '#'}, {'name': 'Login', 'url': '#'}],
        'page_name': 'home'}
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
