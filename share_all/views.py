from django.http import HttpResponse


# Create your views here.
def index(request):
    html = '''
    <script>
    window.location="bookmark"
    </script>
    '''
    return HttpResponse(html)
