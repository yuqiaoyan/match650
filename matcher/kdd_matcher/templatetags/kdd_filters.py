from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='split')
@stringfilter
def split(value, delimiter):
    return value.split(delimiter)


@register.filter(needs_autoescape=True)
@stringfilter
def int_bold(value, interest, autoescape=None):
    new_string = []
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    for item in value.split(' '):
        if item.lower() in interest.lower():
            new_string.append("<strong>%s</strong>" % esc(item))
        else:
            new_string.append("%s" % esc(item))
    result = ' '.join(new_string)
    return mark_safe(result)
