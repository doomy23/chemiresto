from django import template
from django.template import Context, Template, RequestContext
from django.template.loader import render_to_string
register = template.Library()

@register.simple_tag
def headerlogin(request):
    return render_to_string('accounts/header-login.html', {}, context_instance=RequestContext(request))
    