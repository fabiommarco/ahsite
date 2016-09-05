from app.utils import envia_email
from app.models import GeneralConfig

from django.template import loader, Context
from django import forms

class ContactForm(forms.Form):
    name        = forms.CharField()
    email       = forms.EmailField()
    city      = forms.CharField()
    phone    = forms.CharField()
    message    = forms.CharField()

    def send(self,request):
        config = GeneralConfig.objects.latest('id')
        # Body
        th = loader.get_template('emails/contato.html')
        tt = loader.get_template('emails/contato.txt')
        c = Context({
            'name': self.cleaned_data["name"],
            'city': self.cleaned_data["city"],
            'phone': self.cleaned_data["phone"],
            'email': self.cleaned_data["email"],
            'message': self.cleaned_data["message"],
        })
        
        html_body = th.render(c)
        txt_body = tt.render(c)
        envia_email(txt_body, html_body, 
        			subject= 'E-mail de Contato - Site', 
        			to=[config.config_email,], 
        			from_sender="%s <%s>" % (self.cleaned_data["name"], self.cleaned_data["email"]))

