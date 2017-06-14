from django.http import HttpResponse


def get_all_app_url(request):
    from django.conf import settings
    host = request.build_absolute_uri('/') # request.get_host()
    app_urls = [host + name.split('.')[0] for name in settings.INSTALLED_APPS[:-7]]
    return app_urls
 
# Create your views here.
def index(request):
    html = '''
    <script>
    window.location="bookmark"
    </script>
    '''
    #html = str(get_all_app_url(request))
    return HttpResponse(html)
