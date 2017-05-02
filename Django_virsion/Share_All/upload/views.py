from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.contrib.auth.models import User as UserAccount
from .forms import UploadFileForm
import os
from openload import OpenLoad
from .models import File

def index(request):
    context = {
        'files': None,
        'redirect': None
        }
    if not request.user.is_authenticated:
        context['redirect'] = '../../main/login'
    else:
        user=get_object_or_404(UserAccount, username=request.user.username)
        files = user.file_set.all()
        context['files'] = files
    return render(request, 'index.html', context)

def upload(request):
    context = {
        'redirect': None,
        }
    if not request.user.is_authenticated:
        context['redirect'] = '../../main/login'

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(UserAccount, username=request.user.username)
            f = request.FILES['file']
            file_name = request.FILES['file'].name
            path = os.path.join('static/files', file_name)
            with open(path, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            try:
                o = OpenLoad('bd3ad2933dd31c31', 'kW8BDL8v')
                info = o.upload_file(path)['result']
                file = File(user=user, file_name=info['name'], file_id=info['id'], file_url=info['url'])
                file.save()
                os.remove(path)
            except Exception as e:
                os.remove(path)
        context['redirect'] = '..'
    return render(request, 'index.html', context)
