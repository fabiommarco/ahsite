from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings
from app.utils import remove_accents
import math

register = template.Library()

@stringfilter
def get_file_name(value):
    return value.split('/')[-1]
    
@stringfilter
def get_file_type(value):
    return value.split('/')[-1].split('.')[-1].lower()

@stringfilter
def primeiro_paragrafo(value):
    return value[:value.find("</p>")+4]
    
@stringfilter
def restante(value):
    return value[value.find("</p>")+4:]

@stringfilter
def extract_youtube_key(value):
    return value.split('/')[-1].replace('watch?v=', '')[:11]
    
@register.filter('qtd_max')
def qtd_max(ob, form_type):
    return "(M&aacute;ximo: %s)" % settings.MAX[ob.__class__.__name__][form_type.__class__.__name__]
    
@register.filter('total_de_paginas')
def total_de_paginas(obj, max_por_pagina):
    return int(math.ceil(len(obj) / float(max_por_pagina)))
    
@register.filter('remove_acento')
def remove_acento(value):
    return remove_accents(value)
    
@register.filter('blockquote')
def blockquote(value):
    value = value.replace("<blockquote>", "<blockquote><div class=\"blockquote-inner-span\">")
    value = value.replace("</blockquote>", "</div></blockquote>")
    return value
    
register.filter('extract_youtube_key', extract_youtube_key)
register.filter('primeiro_paragrafo', primeiro_paragrafo)
register.filter('restante', restante)
register.filter('get_file_name', get_file_name)
register.filter('get_file_type', get_file_type)
