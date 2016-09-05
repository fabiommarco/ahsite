# -*- coding: utf-8 -*-
"""
    AH Website - LFMarques - 2016
    luizfelipe.unesp@gmail.com
"""
from __future__ import unicode_literals
from django.db import models
# from tinymce import models as tinymce_models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType

import datetime
import uuid

from ckeditor.fields import RichTextField

def get_upload_path(instance, filename):
        f, ext = os.path.splitext(filename)
        new_filename = '%s%s' % (uuid.uuid4().hex, ext)
        return os.path.join('uploads',str(uuid.uuid4()), new_filename)

TIPO_RELATORIO = (
    ('cotacao_agricola', 'Cotação Agrícola'),
    ('relatorio_agricola', 'Relatorio Agricola'),
    ('analise_grafica', 'Analise Gráfica'),
    ('call_macro', 'Call Macro')
    
)
# =================================================
class Imagem(models.Model):

    imagem = models.ImageField("Imagem", upload_to=get_upload_path)
    descricao = models.CharField(u"Descrição breve", max_length=200, blank=True)
    main_image = models.BooleanField(u"Imagem Principal")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    
    class Meta:
        verbose_name_plural = "Galeria de Imagens"
    

class GeneralConfig(models.Model):
    config_street = models.CharField(u"Logradouro", help_text = "Exemplo: Rua Rio Branco",\
                                     max_length = 200, blank = False)
    config_number = models.IntegerField(u"Número", blank = False)
    config_neighbourhood = models.CharField(u"Bairro", help_text = "Exemplo: Vila Falcão",\
                                            max_length = 200, blank = False)
    config_email = models.EmailField(u"Email", help_text = '<strong>Atenção! </strong>Através desse email \
                                        você receberá os contados enviados pelo site.', blank = False)
    config_phone = models.CharField(u"Telefone", help_text = "Formato: (18) 9900-5544",\
                                    max_length = 15, blank = False)
    config_phone_alternative = models.CharField(u"Telefone Alternativo", help_text = "Formato: (18) 9900-5544",\
                                                max_length = 15, blank = True)
    
    config_social_facebook = models.URLField(u'Facebook', help_text = 'Formato: https://www.facebook.com/SUA_PAGINA', blank = True)
    config_social_youtube = models.URLField(u'Youtube', help_text = 'Formato: https://www.youtube.com/user/SEU_CANAL', blank = True)
    config_social_instagram = models.URLField(u'Instagram', help_text = 'Formato: https://www.instagram.com/SEU_PERFIL', blank = True)
        

    class Meta:
        verbose_name_plural = "Configurações Gerais"

    def __unicode__(self):
        return self.config_street


class AboutCompany(models.Model):
    ac_about =  RichTextField(u"Conteúdo do 'Quem Somos'", blank = False)
    ac_vision = RichTextField(u"Conteúdo do 'Visão'", blank = False)
    ac_mission =RichTextField(u"Conteúdo do 'Missão'", blank = False)
    ac_values = RichTextField(u"Conteúdo do 'Valores'", blank = False)
    
    def __unicode__(self):
        return self.ac_about
    
    class Meta:
        verbose_name_plural = u"Sobre a Empresa"


class Event(models.Model):
    event_date = models.DateTimeField(default=datetime.datetime.now)
    event_title = models.CharField(u"Evento", max_length=300)
    event_local = models.CharField(u"Local", max_length=300)
    event_slug = models.SlugField(unique=True, max_length=100, editable=False)
    event_description = models.TextField(u"Descrição")
    event_video = models.CharField("Vídeo do YouTube", max_length=150, blank=True, help_text="Digite a URL do vídeo seguindo este exemplo: <strong>http://www.youtube.com/watch?v=aAkurCTifE0</strong>")

    event_galery_title = models.CharField("Título da Galeria de Imagens", blank=True, max_length=200, help_text="Digite um nome para a Galeria de Imagens, deixe o campo em branco caso queira manter o nome como Galeria de Imagens.")
    event_galery = GenericRelation(Imagem)
    
    def __unicode__(self):
        return self.event_title

    def save(self):
        self.event_slug = slugify(self.event_title)
        super(Event, self).save()

    class Meta:
        verbose_name_plural = u"Eventos"

class Jobs(models.Model):
    job_date = models.DateTimeField(default=datetime.datetime.now)
    job_title = models.CharField(u"Titúlo da Vaga", max_length=300)
    job_description = models.TextField(u"Descrição",help_text='Desreva aqui as especificações da vaga e seus pré-requisitos',\
                                        max_length=300)
    
    def __unicode__(self):
        return self.job_title

    class Meta:
        verbose_name_plural = u"Vagas de Trabalho"

class Magazine(models.Model):
    magazine_date = models.DateTimeField(default=datetime.datetime.now)
    magazine_title = models.CharField(u"Titúlo da Edição", max_length=300)
    magazine_description = RichTextField(u"Descrição",max_length=300,blank=True)
    magazine_file = models.FileField("Arquivo", upload_to=get_upload_path, max_length=100)
    
    def __unicode__(self):
        return self.magazine_title

    class Meta:
        verbose_name_plural = u"Revistas"

class Research(models.Model):
    reserach_date = models.DateField(default=datetime.datetime.now)
    reserach_title = models.CharField(u"Título", max_length=300)
    reserach_type = models.CharField(u"Tipo de Relatorio",choices=TIPO_RELATORIO, max_length=200
                                    ,help_text="O relatório Cotação Agrícola controla a exibição de todos os outro.\
                                    Portanto sempre adicione um Cotação agrícola para validar a exibição de todos.")
    reserach_description = RichTextField(u"Descrição")
    research_file = models.FileField("Arquivo", upload_to=get_upload_path, max_length=100)
    
    class Meta:
       verbose_name_plural = u"Researchs"


class Newsletter(models.Model):
    news_date = models.DateTimeField(default=datetime.datetime.now)
    news_name = models.CharField("Nome",max_length=200)
    news_email = models.EmailField('Email')
    
    def __unicode__(self):
        return self.news_name

class Sale(models.Model):
    sale_description = RichTextField(u"Texto da Página",help_text='Conteúdo da página de Vendas')
    sale_email = models.EmailField('Email',blank=True, help_text='O email do formulário da Página de Vendas será enviado para\
                                                                  o email registrado no menu <a href="/admin/app/generalconfig/">Configurações Gerais</a>.\
                                                                  Use este campo para registrar um email adicional utilizado na Página de Vendas.')
    
    def __unicode__(self):
        return self.sale_description

    class Meta:
        verbose_name_plural = u"Página de Vendas"
