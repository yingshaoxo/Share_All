from django.shortcuts import render

import random


def get_all_app_url(request):
    from django.conf import settings
    # host = request.build_absolute_uri('/') # request.get_host()
    app_urls = [name.split('.')[0] for name in settings.INSTALLED_APPS[:-8]]
    return app_urls
 
# Create your views here.
def index(request):
    colors = ['normal', 'success', 'info', 'warning', 'danger']
    urls = get_all_app_url(request)
    items = []
    for url in urls:
        items.append({'color': random.choice(colors), 'url': url})
    return render(request, 'main/index.html', context={'items': items})
