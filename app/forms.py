# -*- coding: utf-8 -*-
from django.template import loader, Context, RequestContext
from django.shortcuts import render_to_response
from django import forms
from django.conf import settings
from django.forms.util import ErrorList


from app.models import Configuracao
from app.utils import getCoordinates, envia_email

class ConfiguracoesForm(forms.Form):
    nome_da_empresa     = forms.CharField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    titulo_do_site      = forms.CharField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    logomarca           = forms.ImageField(required=False)
    endereco_logradouro = forms.CharField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    cidade              = forms.CharField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    estado              = forms.CharField(widget=forms.Select(choices=settings.ESTADO_CHOICES))
    telefone            = forms.CharField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    email_contato       = forms.EmailField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    cor_layout          = forms.CharField(widget=forms.HiddenInput())
    
    exibe_produtos      = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'vCheckboxLabel'}))
    exibe_servicos      = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'vCheckboxLabel'}))
    exibe_clientes      = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'vCheckboxLabel'}))
    exibe_suporte       = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'vCheckboxLabel'}))
    
    twitter_username    = forms.CharField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    meta_description    = forms.CharField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    meta_keywords       = forms.CharField(widget=forms.TextInput(attrs={'class':'vTextField'}))
    
    google_analytics    = forms.CharField(required=False, widget=forms.Textarea(attrs={'class':'vTextField'}))
    google_webmaster    = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    
    exibe_mapa_contato  = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'vCheckboxLabel'}))
    google_maps         = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    
    def clean_logomarca(self):
        # Validando se a logomarca foi escolhida
        if not self.files.has_key("logomarca") and Configuracao.objects.get(chave="logomarca").valor is '':
            raise forms.ValidationError(u'A logomarca é obrigatória')
        elif self.files.has_key("logomarca"):
            from PIL import Image
            image_size = Image.open(self.files["logomarca"]).size
            if (not image_size[0] <= 310) or (not image_size[1] == 95):
                raise forms.ValidationError(u'Por favor, insira a logomarca na proporção: largura <= 310px e altura = 95px.')
    
    def clean_twitter_username(self):
        twitter_username = self.cleaned_data["twitter_username"]
        if "@" not in twitter_username:
            raise forms.ValidationError(u'Por favor, insira o nome de usuário com a @')
        elif twitter_username.index("@") <> 0:
            raise forms.ValidationError(u'Por favor, a @ deve estar no início do nome de usuário')
        return twitter_username    
    
    def clean(self):
        # Validando se tem ao menos uma opcao marcada entre Exibir Produtos e Exibir Serviços
        cleaned_data = self.cleaned_data

        if not cleaned_data["exibe_produtos"] and not cleaned_data["exibe_servicos"]:
            self.errors["exibe_servicos"] = ErrorList([u"Por favor, você deve marcar ao menos *uma* das páginas de Produto ou Serviços."])
            
        # Validando se a chave do Google Maps foi informada, caso o mapa deva ser exibido na pagina de contato
        if cleaned_data["exibe_mapa_contato"] and not cleaned_data["google_maps"]:
            self.errors["google_maps"] = ErrorList([u"Por favor, informe a chave do Google Maps caso queira mostrar o mapa na página de Contato."])
        
        return cleaned_data
    
    def save(self):
        """ Função que salva o Formulário """
        for field in self.cleaned_data:
            configuracao = Configuracao.objects.get(chave=field)
            
            # Salvando todos os dados com exceção da Logomarca
            if field <> "logomarca":
                configuracao.valor = self.cleaned_data[field]
                configuracao.save()
        
        # Recuperando as coordenadas baseado no Endereço
        latitude, longitude = getCoordinates(self.cleaned_data["endereco_logradouro"] + 
                                             " " +
                                             self.cleaned_data["cidade"] + 
                                             " - " + 
                                             self.cleaned_data["estado"])
                                             
        mapa_latitude = Configuracao.objects.get(chave="mapa_latitude")
        mapa_longitude = Configuracao.objects.get(chave="mapa_longitude")
        
        mapa_latitude.valor = latitude
        mapa_longitude.valor = longitude
        
        mapa_latitude.save()
        mapa_longitude.save()
        
        # Salvando o arquivo
        if self.files.has_key("logomarca"):
            f = self.files["logomarca"]
            
            # Encontrando o caminho da logomarca
            path = settings.UPLOADS_ROOT + "logomarca/"+ f.name
            
            # Salvando a logomarca normal
            destination = open(path, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()

            # Salvando a configuração da logomarca
            logomarca = Configuracao.objects.get(chave="logomarca")
            logomarca.valor = "/media/uploads/logomarca/" + f.name
            logomarca.save()
            
            # Salvando a logomarca pequena
            from PIL import Image
            import glob, os
            size = 155, 48
            file, ext = os.path.splitext(path)
            im = Image.open(path)
            im.thumbnail(size, Image.ANTIALIAS)
            
            extensao = ext.replace(".", "")
            if extensao == u'jpg':
                extensao = u"jpeg"
                
            im.save(file + "-small." + extensao, extensao)
            
            logomarca_pequena = Configuracao.objects.get(chave="logomarca_pequena")
            logomarca_pequena.valor = "/media/uploads/logomarca/" + file.split("/")[-1] + "-small." + extensao
            logomarca_pequena.save()
            
class RedesSociaisForm(forms.Form):
    orkut       = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    facebook    = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    youtube     = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    flickr      = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    linkedin    = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    delicious   = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    digg        = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    twitter     = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    myspace     = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    formspring  = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))
    blog        = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'vTextField'}))

    def clean(self):
        # Validando se tem ao menos 3 redes sociais
        cleaned_data = self.cleaned_data
        
        quantidade_validada = 0
        for field in cleaned_data:
            if cleaned_data[field] is not u'':
                quantidade_validada += 1
        
        if quantidade_validada < 3 or quantidade_validada > 6:
            raise forms.ValidationError('Por favor, você deve cadastrar de 3 a 6 redes sociais.')
        
        print "shit"
        
        return cleaned_data

    def save(self):
        """ Função que salva o Formulário """
        for field in self.cleaned_data:
            configuracao = Configuracao.objects.get(chave=field)

            # Salvando todos os dados com exceção da Logomarca
            configuracao.valor = self.cleaned_data[field]
            configuracao.save()
            
class NewsletterForm(forms.Form):
    nome     = forms.CharField()
    email    = forms.EmailField()
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if Newsletter.objects.filter(email=email):
            raise forms.ValidationError("E-mail já existente.")
        return email
        
    def save(self):
        """Função que salva o Formulário"""
        newsletter = Newsletter(nome=self.cleaned_data["nome"], email=self.cleaned_data["email"])
        newsletter.save()
        
class ContatoForm(forms.Form):
    nome        = forms.CharField()
    cidade      = forms.CharField(required=False)
    telefone    = forms.CharField(required=False)
    email       = forms.EmailField()
    mensagem    = forms.CharField()

    def send(self, configuracoes):
        """Função que salva e Envia o Formulário"""
        
        import datetime
        
        # Body
        th = loader.get_template('emails/contato.html')
        tt = loader.get_template('emails/contato.txt')
        c = Context({
            'configuracoes': configuracoes["configuracoes"],
            'nome': self.cleaned_data["nome"],
            'email': self.cleaned_data["email"],
            'cidade': self.cleaned_data["cidade"],
            'telefone': self.cleaned_data["telefone"],
            'mensagem': self.cleaned_data["mensagem"],
            'hora': datetime.datetime.now()
        })
        
        # Renderizando e enviando o e-mail
        html_body = th.render(c)
        txt_body = tt.render(c)
        envia_email(txt_body, html_body, subject= 'E-mail de Contato - %s' % configuracoes["configuracoes"]["nome_da_empresa"], to=[configuracoes["configuracoes"]["email_contato"], 'victorcinaglia@gmail.com'], from_sender="%s <%s>" % (self.cleaned_data["nome"], self.cleaned_data["email"]))
        
