from django.shortcuts import render as _render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.context_processors import csrf

def render(request, url="", context={}):
    context['loginpartial'] = login_partial(request)
    return _render(request, url, context_instance = RequestContext(request, context))

def login_partial(request):
    return render_to_string('loginpartial.html',
        {
            'user': request.user,
            'csrf_token': csrf(request),
        }
    )