# -*- coding: utf-8 -*-
from app.models import Banner
import math,time
import unicodedata

def remove_accents(str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])


# Funcao que envia e-mails com dois bodies (html/txt)
def envia_email(txt_body, html_body, subject='E-mail de Contato', from_sender='no-reply@maximize-ti.com.br', to=[]):
    from django.core.mail import EmailMultiAlternatives

    # Funcao de envio do E-mail
    msg = EmailMultiAlternatives(subject, txt_body, from_sender, to, headers = {'Reply-To': from_sender})
    msg.attach_alternative(html_body, "text/html")
    return msg.send()

def getRelativeTimeStr(str_time,time_format="%m/%d/%y %H%M",accuracy=1,cmp_time=None,alternative_past=None):
    # convert str_time to date
    t = time.mktime(time.strptime(str_time,time_format))
    return getRelativeTime(t,accuracy=accuracy,cmp_time=cmp_time,alternative_past=alternative_past)

def getRelativeTime(t,accuracy=1,cmp_time=None,alternative_past=None):
    if cmp_time==None:
        cmp_time = time.time()
    diff_seconds = (t - cmp_time) + 20 # unknown why it's off by 20 seconds
    diff_minutes = int(math.floor(diff_seconds/60))
    relative_time = ""

    sign = diff_minutes > 0
    diff_minutes = math.fabs(diff_minutes)
    # return in minutes
    if diff_minutes > (60 * 24):
        relative_time = str(int(math.floor(diff_minutes / (60*24)))) + " dias"
        if accuracy > 1:
            relative_time +=" "+ str(int(math.floor((diff_minutes % (60*24))) / 60)) + " horas"
    elif diff_minutes > 60 :
        relative_time = str(int(math.floor(diff_minutes / 60))) + " horas"
        if accuracy > 1:
            relative_time +=" "+ str(int(diff_minutes % 60)) + " minutos"
    else:
        relative_time = str(int(diff_minutes)) + " minutos"

    if sign:
        relative_time = relative_time
    else:
        if alternative_past:
            return alternative_past
        relative_time += " atrás"
    return relative_time
    
def getCoordinates(address):
    """Get the coordinates based on an address provided """
    import urllib
    import simplejson
    import socket

    # Requisicao nao pode durar mais que 5 segundos
    socket.setdefaulttimeout(5)

    try: 
        url = remove_accents(u"http://maps.google.com/maps/geo?q=%s" % unicode(address).replace(' ', '+'))
        
        # Fazendo a requisicao
        f = urllib.urlopen(url)
        response = f.read()
    
        # Parsing o json
        parsed_json = simplejson.loads(response)
        
        # Coordinates
        coordinates = parsed_json["Placemark"][0]["Point"]["coordinates"]
        
        return coordinates[0], coordinates[1]
        
    except:
        pass
            
    return 0, 0

def getTwitts(username, quantity):
    """ Retorna twitts de um usuario """
    import urllib
    import simplejson
    import socket
    import re
    
    # Requisicao nao pode durar mais que 5 segundos
    socket.setdefaulttimeout(5)
    
    try:
        # Fazendo a requisicao
        f = urllib.urlopen("http://api.twitter.com/1/statuses/user_timeline.json?screen_name=" + username.replace("@", ""))
        response = f.read()
    
        # Parsing o json
        parsed_json = simplejson.loads(response)

        # Parsing a data
        import time
        DATETIME_STRING_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'
        for item in parsed_json:
            tmp = time.strptime(item["created_at"], DATETIME_STRING_FORMAT)
            tmp = time.strftime("%Y-%m-%d %H:%M:%S", tmp)
            item["created_at"] = getRelativeTimeStr(tmp, time_format="%Y-%m-%d %H:%M:%S")

            # Convertendo as urls
            r1 = r"(^|[\n ])([\w]+?://[\w]+[^ \"\n\r\t< ]*)"
            item["text"] = re.sub(r1, r'<a rel="blank" href="\2">\2</a>', item["text"])
            
            r2 = r"(^|[\n ])((www|ftp)\.[^ \"\t\n\r< ]*)"
            item["text"] = re.sub(r2, r'<a rel="blank" href="http://\2">\2</a>', item["text"])
            
            
            # Convertendo as hashtags em links
            item["text"] = re.sub(r'#(?P<hashtag>[a-zA-Z_0-9]+)', r'<a href="http://twitter.com/search?q=%23\g<hashtag>" rel="blank" title="#\g<hashtag>">#\g<hashtag></a>', item["text"])
            item["text"] = re.sub(r'@(?P<person>[a-zA-Z_0-9]+)', r'<a href="http://twitter.com/\g<person>" rel="blank" title="@\g<person>">@\g<person></a>', item["text"])
            
    except:
        parsed_json = []
    
    return parsed_json[:quantity]
    
def getBanner(nome_da_pagina=""):
    """ Retorna o Banner da Página passada por Parametro"""
    banner = Banner.objects.filter(pagina=nome_da_pagina)
    if len(banner) == 1:
        return banner[0].banner
    else:
        banner = Banner.objects.filter(principal=True)
        if len(banner) == 1:
            return banner[0].banner
        else:
            return None
