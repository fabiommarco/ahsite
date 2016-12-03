# -*- coding: utf-8 -*-
"""
    AH Website - LFMarques - 2016
    luizfelipe.unesp@gmail.com
"""
from __future__ import unicode_literals

import datetime
import uuid
import os

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from django.utils import translation
from django.template.defaultfilters import truncatechars,slugify
from ckeditor.fields import RichTextField
from django.conf import settings

TIPO_RELATORIO = (
    ('cotacao_agricola', 'Cotação Agrícola'),
    ('relatorio_agricola', 'Relatorio Agricola'),
    ('analise_grafica', 'Analise Gráfica'),
    ('call_macro', 'Call Macro')
)


def get_upload_path(instance, filename):
    _f, ext = os.path.splitext(filename)
    new_filename = '%s%s' % (uuid.uuid4().hex, ext)
    return os.path.join('uploads', str(uuid.uuid4()), new_filename)


class TranslatableManager(models.Manager):

    def get_queryset(self):
        return super(TranslatableManager, self).get_queryset().filter(
            language=translation.get_language())


class TranslatableModelBase(models.Model):
    language = models.CharField('Idioma', choices=settings.LANGUAGES,
                                max_length=5,
                                default='pt',
                                blank=False, null=False,
                                help_text='Idioma em que a página será exibida',)

    parent = models.ForeignKey('self',
                               verbose_name=u'Página Original',
                               blank=True, null=True,
                               limit_choices_to={'language': 'pt'},
                               help_text=u'Página da qual esta é uma tradução. '
                                          'Não é necessário para páginas em Português')

    objects = models.Manager()
    translated_objects = TranslatableManager()

    class Meta:
        abstract = True

# =================================================

class Imagem(models.Model):
    imagem = models.ImageField("Imagem", upload_to=get_upload_path)
    descricao = models.CharField(u"Descrição breve", max_length=200, blank=True)
    main_image = models.BooleanField(u"Imagem Principal")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = u"Galeria de Imagens"
        verbose_name_plural = u"Galeria de Imagens"

class Attachment(models.Model):
    attach = models.FileField("Anexo", upload_to=get_upload_path, max_length=100)

    # Generic ForeignKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = "Arquivos Anexos"


class GeneralConfig(models.Model):
    config_street = models.CharField(
        u"Logradouro",
        help_text="Exemplo: Rua Rio Branco",
        max_length=200,
        blank=False)
    config_number = models.IntegerField(u"Número", blank=False)
    config_neighbourhood = models.CharField(
        u"Bairro",
        help_text="Exemplo: Vila Falcão",
        max_length=200,
        blank=False)

    config_email = models.EmailField(
        u"Email",
        help_text='<strong>Atenção! </strong>Através'
                  'desse email você receberá os contados'
                  'enviados pelo site.',
        blank=False)
    config_email_cv = models.EmailField(
        u"Email de Curriculos",
        help_text='Utilize esse campo caso queira registrar um email personalizado'
                  'para recebimento de Curriculos',
        )

    config_phone = models.CharField(
        u"Telefone",
        help_text="Formato: (18) 9900-5544",
        max_length=15,
        blank=False)
    config_phone_alternative = models.CharField(
        u"Telefone Alternativo",
        help_text="Formato: (18) 9900-5544",
        max_length=15,
        blank=True)
    config_social_facebook = models.URLField(
        u'Facebook',
        help_text='Formato: https://www.facebook.com/SUA_PAGINA',
        blank=True)
    config_social_twitter = models.URLField(
        u'Twitter',
        help_text='Formato: https://www.twitter.com/SUA_PAGINA',
        blank=True)
    config_social_youtube = models.URLField(
        u'Youtube',
        help_text='Formato: https://www.youtube.com/user/SEU_CANAL',
        blank=True)
    config_social_instagram = models.URLField(
        u'Instagram',
        help_text='Formato: https://www.instagram.com/SEU_PERFIL',
        blank=True)
    config_social_linkedin = models.URLField(
        u'Linkedin',
        help_text='Formato: https://www.linkedin.com/SEU_PERFIL',
        blank=True)

    class Meta:
        verbose_name = u"Configuração Geral"
        verbose_name_plural = "Configurações Gerais"

    def __unicode__(self):
        return self.config_street


class AboutCompany(TranslatableModelBase):
    ac_content = RichTextField(u"Conteúdo da página", blank=False)
    gallery_title = models.CharField(
        "Título da Galeria de Imagens",
        blank=True,
        max_length=200,
        help_text="Digite um nome para a Galeria de Imagens, deixe o campo em"
                  "branco caso queira manter o nome como Galeria de Imagens.")
    gallery = GenericRelation(Imagem)
    attach_galery = GenericRelation(Attachment)

    def scaped_html(self):
        text = format_html(self.ac_content)
        try:
            text = truncatechars(
                self.ac_content.split('<p>', 1)[1].split('</p>')[0], 100)
        except Exception, e:
            pass
        return text
    scaped_html.allow_tags = True

    def __unicode__(self):
        return self.ac_content

    class Meta:
        verbose_name = u"Sobre a Empresa"
        verbose_name_plural = u"Sobre a Empresa"


class Event(TranslatableModelBase):
    '''
        called as resposabilidade social in the system
    '''
    event_date = models.DateTimeField(u"Data", default=datetime.datetime.now)
    event_title = models.CharField(u"Título", max_length=300)
    event_local = models.CharField(u"Local", max_length=300)
    event_slug = models.SlugField(unique=True, max_length=100, editable=False)
    event_description = RichTextField(u"Descrição")
    event_video = models.CharField(
        "Vídeo do YouTube",
        max_length=150,
        blank=True,
        help_text="Digite somente a parte em <strong>negrito</strong> da URL do vídeo"
        "seguindo este exemplo:http://www.youtube.com/watch?v=<strong>aAkurCTifE0</strong>")
    event_thumbnail = models.ImageField(u"Thumbnail", upload_to=get_upload_path)
    event_galery_title = models.CharField(
        "Título da Galeria de Imagens",
        blank=True,
        max_length=200,
        help_text="Digite um nome para a Galeria de Imagens,"
        " deixe o campo em branco caso queira manter o nome como Galeria de Imagens.")
    event_galery = GenericRelation(Imagem)

    event_attach_galery_title = models.CharField(
        "Título da Galeria de Anexos",
        blank=True,
        max_length=200,
        help_text="Digite um nome para a Galeria de Anexos,"
        " deixe o campo em branco caso queira manter o nome como Galeria de Anexos.")

    event_attach_galery = GenericRelation(Attachment)

    def __unicode__(self):
        return self.event_title

    def save(self):
        self.event_slug = slugify(self.event_title)
        super(Event, self).save()

    class Meta:
        verbose_name = u"Responsabilidade Social"
        verbose_name_plural = u"Responsabilidade Social"

class EnvironmentalResponsability(TranslatableModelBase):
    environ_date = models.DateTimeField(u"Data", default=datetime.datetime.now)
    environ_title = models.CharField(u"Título", max_length=300)
    environ_description = RichTextField(u"Descrição")
    environ_video = models.CharField(
        "Vídeo do YouTube",
        max_length=150,
        blank=True,
        help_text="Digite somente a parte em <strong>negrito</strong> da URL do vídeo"
        "seguindo este exemplo:http://www.youtube.com/watch?v=<strong>aAkurCTifE0</strong>")
    # environ_thumbnail = models.ImageField(u"Thumbnail", upload_to=get_upload_path)
    environ_galery_title = models.CharField(
        "Título da Galeria de Imagens",
        blank=True,
        max_length=200,
        help_text="Digite um nome para a Galeria de Imagens,"
        " deixe o campo em branco caso queira manter o nome como Galeria de Imagens.")
    environ_galery = GenericRelation(Imagem)

    attach_galery_title = models.CharField(
        "Título da Galeria de Anexos",
        blank=True,
        max_length=200,
        help_text="Digite um nome para a Galeria de Anexos,"
        " deixe o campo em branco caso queira manter o nome como Galeria de Anexos.")

    attach_galery = GenericRelation(Attachment)

    def __unicode__(self):
        return self.environ_title

    class Meta:
        verbose_name = u"Responsabilidade Ambiental"
        verbose_name_plural = u"Responsabilidade Ambiental"

class News(TranslatableModelBase):
    news_date = models.DateTimeField()
    news_title = models.CharField(u"Titúlo da Notícia", max_length=300)
    news_slug = models.SlugField(unique=True, max_length=100, editable=False)
    news_description = RichTextField(u"Descrição")
    news_video = models.CharField(
        "Vídeo do YouTube",
        max_length=150,
        blank=True,
        help_text="Digite somente a parte em <strong>negrito</strong> da URL do vídeo"
        "seguindo este exemplo:http://www.youtube.com/watch?v=<strong>aAkurCTifE0</strong>")

    news_galery_title = models.CharField(
        "Título da Galeria de Imagens",
        blank=True,
        max_length=200,
        help_text="Digite um nome para a Galeria de Imagens, "
        "deixe o campo em branco caso queira manter o nome como Galeria de Imagens.")
    news_galery = GenericRelation(Imagem)

    attach_galery_title = models.CharField(
        "Título da Galeria de Anexos",
        blank=True,
        max_length=200,
        help_text="Digite um nome para a Galeria de Anexos,"
        " deixe o campo em branco caso queira manter o nome como Galeria de Anexos.")

    attach_galery = GenericRelation(Attachment)


    def __unicode__(self):
        return self.news_title

    def save(self):
        self.news_slug = slugify(self.news_title)
        super(News, self).save()

    class Meta:
        verbose_name = u"Notícia"
        verbose_name_plural = u"Notícias"

class Partners(TranslatableModelBase):
    partner_date = models.DateTimeField(default=datetime.datetime.now)
    partner_title = models.CharField(u"Nome da Parceria", max_length=300)
    partner_slug = models.SlugField(unique=True, max_length=100, editable=False)
    partner_description = RichTextField(u"Descrição")

    def __unicode__(self):
        return self.partner_title

    def save(self):
        self.partner_slug = slugify(self.partner_title)
        super(Partners, self).save()

    class Meta:
        verbose_name = u"Parceria"
        verbose_name_plural = u"Parcerias"

class Jobs(models.Model):
    job_date = models.DateTimeField(default=datetime.datetime.now)
    job_title = models.CharField(u"Titúlo da Vaga", max_length=300)
    job_description = RichTextField(
        u"Descrição",
        help_text='Desreva aqui as especificações da vaga e seus pré-requisitos')

    def __unicode__(self):
        return self.job_title

    class Meta:
        verbose_name = u"Vaga de Trabalho"
        verbose_name_plural = u"Vagas de Trabalho"

class Magazine(models.Model):
    magazine_date = models.DateTimeField()
    magazine_title = models.CharField(u"Titúlo da Edição", max_length=300)
    magazine_description = RichTextField(u"Descrição", max_length=300, blank=True)
    magazine_file = models.FileField("Arquivo", upload_to=get_upload_path)

    def __unicode__(self):
        return self.magazine_title

    class Meta:
        verbose_name = u"Revista"
        verbose_name_plural = u"Revistas"

class Research(models.Model):
    reserach_date = models.DateField(default=datetime.datetime.now)
    reserach_title = models.CharField(u"Título", max_length=300)
    reserach_type = models.CharField(
        u"Tipo de Relatorio",
        choices=TIPO_RELATORIO,
        max_length=200)
    research_file = models.FileField("Arquivo", upload_to=get_upload_path, max_length=100)

    class Meta:
        verbose_name_plural = u"Researchs"


class Newsletter(models.Model):
    news_date = models.DateTimeField(default=datetime.datetime.now)
    news_name = models.CharField("Nome", max_length=200)
    news_email = models.EmailField('Email')

    def __unicode__(self):
        return self.news_name

class Sale(TranslatableModelBase):
    sale_description = RichTextField(u"Texto da Página", help_text='Conteúdo da página de Vendas')
    sale_email = models.EmailField(
        u'Email',
        blank=True,
        help_text='O email do formulário da Página de Vendas será enviado para'
                  'o email registrado no menu <a href="/admin/app/generalconfig/">Configurações Gerais</a>.'
                  'Use este campo para registrar um email adicional utilizado na Página de Vendas.')

    def __unicode__(self):
        return self.sale_description

    class Meta:
        verbose_name = u"Página de Venda"
        verbose_name_plural = u"Página de Vendas"

class AgriculturalFiles(models.Model):
    ap_date = models.DateTimeField()
    ap_file = models.FileField("Arquivo", upload_to=get_upload_path)
    ap_brief_desc = models.CharField(u"Descrição", max_length=150, blank=True)

    def __unicode__(self):
        return self.ap_brief_desc

    class Meta:
        verbose_name = u"Cotação Agrícola"
        verbose_name_plural = u"Cotações Agrícolas"

class Products(TranslatableModelBase):
    product_date = models.DateTimeField(default=datetime.datetime.now)
    product_name = models.CharField("Nome do Produto", max_length=200)
    product_slug = models.SlugField(unique=True, max_length=100, editable=False)
    product_description = RichTextField(u"Descrição")
    product_category = models.CharField(
        'Categoria',
        choices=(
            ('suinos', 'Suinos'),
            ('bovinos', 'Bovinos'),
            ('cafe', u'Café')
        ),
        max_length=20,
        blank=False, null=False,
        help_text='Categoria do produto')
    product_short_description = models.TextField(
        u"Descrição Curta",
        help_text='Essa descrição irá aparecer na homepage.',
        max_length=200)
    product_galery_title = models.CharField(
        "Título da Galeria de Imagens",
        blank=True,
        max_length=200,
        help_text="Digite um nome para a Galeria de Imagens, deixe o campo em branco caso queira"
                  "manter o nome como Galeria de Imagens.")
    product_galery = GenericRelation(Imagem)

    def save(self):
        self.product_slug = slugify(self.product_name)
        super(Products, self).save()

    def __unicode__(self):
        return self.product_name

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
