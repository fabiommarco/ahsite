# -*- coding: utf-8 -*-
from app.models import GeneralConfig, Jobs, Newsletter
from app.utils import envia_email
from django import forms
from django.template import Context, loader


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    city = forms.CharField()
    phone = forms.CharField()
    message = forms.CharField()

    def send(self, request, extra_recipient=None):
        config = GeneralConfig.objects.latest("id")
        # Body
        th = loader.get_template("emails/contato.html")
        tt = loader.get_template("emails/contato.txt")
        c = Context(
            {
                "name": self.cleaned_data["name"],
                "city": self.cleaned_data["city"],
                "phone": self.cleaned_data["phone"],
                "email": self.cleaned_data["email"],
                "message": self.cleaned_data["message"],
            }
        )

        html_body = th.render(c)
        txt_body = tt.render(c)
        to = [config.config_email]
        if extra_recipient:
            to.append(extra_recipient)
        envia_email(
            txt_body,
            html_body,
            subject="E-mail de Contato - Site",
            to=to,
            from_sender="%s <%s>"
            % (self.cleaned_data["name"], self.cleaned_data["email"]),
        )


class ApplyJobForm(ContactForm):
    attach = forms.FileField()
    # job_id = forms.HiddenInput()
    job_id = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(ApplyJobForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
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
        c = Context(
            {
                "name": self.cleaned_data["name"],
                "city": self.cleaned_data["city"],
                "phone": self.cleaned_data["phone"],
                "email": self.cleaned_data["email"],
                "message": self.cleaned_data["message"],
                "job_title": job.job_title,
            }
        )

        html_body = th.render(c)
        txt_body = tt.render(c)
        envia_email(
            txt_body,
            html_body,
            subject="E-mail de Candidatura Vaga - Site",
            to=recipients,
            attach=cv,
            from_sender="%s <%s>"
            % (self.cleaned_data["name"], self.cleaned_data["email"]),
        )


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
