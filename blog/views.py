from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import TesteForm


# Create your views here.

def index(request):
    return render(request, 'base_blog.html')


def create(request):
    data = dict()
    form = TesteForm()
    context = {
        'form': form
    }

    data['html_form'] = render_to_string('blog/blog.html', context=context,
                                         request=request)

    return JsonResponse(data)
