from django.shortcuts import render

from . import handle_diary as handle

# Create your views here.
def index(request):
    context = {
        'years': None,
        'content': None
        }
    years, content = handle.get_content()
    context.update({'years': years, 'content': content})
    return render(request, 'diary/index.html', context)
