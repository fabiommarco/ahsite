# -*- coding: utf-8 -*-
from app.models import GeneralConfig, Jobs, Newsletter, EquipeCompras
from app.utils import envia_email
from django import forms
from django.template import loader


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    city = forms.CharField()
    phone = forms.CharField()
    message = forms.CharField()
    destinatario = forms.CharField()

    def clean_destinatario(self):
        destinatario = self.cleaned_data["destinatario"]
        
        # E-mails hardcoded existentes
        emails_validos = [
            "cristiano.dutra@ah.agr.br", 
            "willian.rodrigues@ah.agr.br", 
            "alexandre.brazoloto@ah.agr.br",
            "ambos",
            "todos"  # Para enviar para todos os responsáveis
        ]
        
        # Adicionar e-mails da equipe de compras ativa
        equipe_emails = EquipeCompras.objects.filter(ativo=True).values_list('email', flat=True)
        emails_validos.extend(equipe_emails)
        
        if destinatario not in emails_validos:
            raise forms.ValidationError("Por favor, selecione um destinatário válido.")
        return destinatario

    def send(self, request, extra_recipient=None):
        config = GeneralConfig.objects.latest("id")
        th = loader.get_template("emails/contato.html")
        tt = loader.get_template("emails/contato.txt")
        c = {
            "name": self.cleaned_data["name"],
            "city": self.cleaned_data["city"],
            "phone": self.cleaned_data["phone"],
            "email": self.cleaned_data["email"],
            "message": self.cleaned_data["message"],
        }
        html_body = th.render(c)
        txt_body = tt.render(c)
        destinatario = self.cleaned_data["destinatario"]
        
        if destinatario == "ambos":
            to = ["cristiano.dutra@ah.agr.br", "willian.rodrigues@ah.agr.br"]
        elif destinatario == "todos":
            # Enviar para todos os membros ativos da equipe de compras
            to = list(EquipeCompras.objects.filter(ativo=True).values_list('email', flat=True))
        else:
            to = [destinatario]
        
        try:
            envia_email(
                txt_body,
                html_body,
                subject="E-mail de Contato - Site",
                to=to,
                from_sender="Agropecuária AH <ti@ah.agr.br>",
            )
            return True, ""
        except Exception as e:
            return False, str(e)


class ApplyJobForm(ContactForm):
    attach = forms.FileField()
    job_id = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ApplyJobForm, self).__init__(*args, **kwargs)
        # Definindo a ordem dos campos usando field_order
        self.field_order = [
            "name",
            "email",
            "phone",
            "city",
            "attach",
            "message",
            "job_id",
        ]

    def send(self, request):
        config = GeneralConfig.objects.latest("id")
        recipients = [config.config_email]
        if config.config_email_cv:
            recipients.append(config.config_email_cv)

        job = Jobs.objects.get(id=self.cleaned_data["job_id"])
        cv = self.cleaned_data["attach"]
        # Body
        th = loader.get_template("emails/trabalhe.html")
        tt = loader.get_template("emails/trabalhe.txt")
        c = {
            "name": self.cleaned_data["name"],
            "city": self.cleaned_data["city"],
            "phone": self.cleaned_data["phone"],
            "email": self.cleaned_data["email"],
            "message": self.cleaned_data["message"],
            "job_title": job.job_title,
        }

        html_body = th.render(c)
        txt_body = tt.render(c)
        try:
            envia_email(
                txt_body,
                html_body,
                subject="E-mail de Candidatura Vaga - Site",
                to=recipients,
                attach=cv,
                from_sender="Agropecuária AH <ti@ah.agr.br>",
            )
            return True, ""
        except Exception as e:
            return False, str(e)


class NewsletterForm(forms.Form):
    nome = forms.CharField()
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Newsletter.objects.filter(news_email=email):
            raise forms.ValidationError("E-mail já existente.")
        return email

    def save(self):
        newsletter = Newsletter(
            news_name=self.cleaned_data["nome"], news_email=self.cleaned_data["email"]
        )
        newsletter.save()
