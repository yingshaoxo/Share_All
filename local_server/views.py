from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import handle_url as handle

# Create your views here.
def receive_url(request, path):
    handle.write_url(path)
    return HttpResponse(path)

def index(request):
    local_url = handle.read_url()
    if local_url:
        return redirect(local_url)
    else:
        return HttpResponse('Local server not ready yet.')
