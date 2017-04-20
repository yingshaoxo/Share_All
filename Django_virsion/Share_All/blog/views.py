from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    html = '''
    <script>
    window.location="http://yingshaoxo.cf"
    </script>
    '''
    return HttpResponse(html)
