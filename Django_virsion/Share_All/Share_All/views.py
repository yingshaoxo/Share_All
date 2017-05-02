from django.http import HttpResponse

def index(request):
    html = '''
    <script>
    window.location="main"
    </script>
    '''
    return HttpResponse(html)



