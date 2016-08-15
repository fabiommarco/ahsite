# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
# from sorl.thumbnail.fields import ImageWithThumbnailsField
import datetime

class Imagem(models.Model):
    imagem = models.ImageField("Imagem", upload_to='uploads/galerias/', max_length=100)
    # imagem = ImageWithThumbnailsField(
    #     upload_to='uploads/galerias/',
    #     thumbnail={
    #         'size': (270, 210),
    #         'options': ('pad',)
	     	
    #     },
    #     extra_thumbnails={
    #         # Produtos e Servicos
    #         'catalogo': {
    #             'size': (300, 120),
    #             'options': ('pad',)
    #         },
    #         'catalogo_servicos': {
    #             'size': (280, 120),
    #             'options': ('pad',)
    #         },
    #         'miniaturas': {
    #             'size': (70, 50),
    #             'options': ('pad',)
    #         },
    #         'home': {
    #             'size': (100, 100),
    #             'options': ('pad',)
    #         },
    #         'produto_big': {
    #             'size': (500, 500),
    #             'options': ('pad',)
    #         },
            
    #         # Noticias
    #         'noticia_small': {
    #             'size': (100, 100),
    #             'options': ('pad',)
    #         },
    #         'noticia_medium': {
    #             'size': (250, 200),
    #         },
    #         'noticia_big': {
    #             'size': (500, 500),
    #         },
            
    #         # Quem Somos
    #         'quem_somos_small': {
    #             'size': (130, 100),
    #             'options': ('pad',)
    #         },
    #         'big': {
    #             'size': (500, 500),
    #             'options': ('pad',)
    #         },
    #     },
    # )
    
    descricao = models.CharField(u"Descrição breve", max_length=200, blank=True)
    imagem_principal = models.BooleanField()
    
    # Generic ForeignKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = "Galeria de Imagens"
    

class Noticia(models.Model):
    data = models.DateTimeField(default=datetime.datetime.now)
    titulo = models.CharField(u"Notícia", max_length=300)
    slug = models.SlugField(unique=True, max_length=100, editable=False)

    conteudo = models.TextField("Conteúdo")
    titulo_galeria = models.CharField("Título da Galeria de Imagens", blank=True, max_length=200, help_text="Digite um nome para a Galeria de Imagens, deixe o campo em branco caso queira manter o nome como Galeria de Imagens.")
    video = models.CharField("Vídeo do YouTube", max_length=150, blank=True, help_text="Digite a URL do vídeo seguindo este exemplo: <strong>http://www.youtube.com/watch?v=aAkurCTifE0</strong>")
    
    # Generic ForeignKey
    imagens = generic.GenericRelation(Imagem)
   # anexos = generic.GenericRelation(Anexo)
    
    # Mostra imagem principal
    mostra_principal = models.BooleanField(default=False, verbose_name="Mostra imagem principal no corpo?", help_text="Marque aqui caso queira que a imagem principal apareça no corpo da notícia. A imagem será anexada abaixo do <strong>primeiro paragrafo</strong>.")
    
    # Estatisticas
    visitas = models.IntegerField(default=0, editable=False)
    
    def get_absolute_url(self):
        return "/noticias/%i/%s" % (self.id, self.slug)
    
    # Retorna a imagem principal
    def imagem_principal(self):
        """ Retorna a imagem principal, se existir """
        try:
            return self.imagens.get(imagem_principal=True)
        except:
            return settings.MEDIA_URL + '/images/no-images.gif'
    
    # Retorna o primeiro paragrafo da notícia
    def primeiro_paragrafo(self):
        """Retorna o Primeiro Paragrafo da Notícia"""
        primeiro_paragrafo = list(self.conteudo.partition('</p>'))
        return ''.join([primeiro_paragrafo[0], primeiro_paragrafo[1]])
    
    def get_absolute_url(self):
        return "/noticias/%i/%s" % (self.id, self.slug)
    
    def __unicode__(self):
        return self.titulo
    
    # Método customizado para salvar o SLUG
    def save(self):
        self.slug = slugify(self.titulo)
        super(Noticia, self).save()
    
    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = u"Notícias"


class Anexo(models.Model):
    anexo = models.FileField("Anexo", upload_to='uploads/anexos/', max_length=100)
    descricao = models.CharField(u"Descrição breve", max_length=200, blank=True)
    
    # Generic ForeignKey
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = "Arquivos Anexos"

class Cliente(models.Model):
    nome = models.CharField("Nome do Cliente", max_length=200)
    data = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique=True, max_length=100, editable=False)

    descricao = models.TextField(u"Descrição do Cliente")
    website = models.URLField(blank=True, null=True, verify_exists=True, help_text="Informe o site do cliente, caso ele possua.")
    video = models.CharField("Vídeo do YouTube", max_length=150, blank=True, help_text="Digite a URL do vídeo seguindo este exemplo: <strong>http://www.youtube.com/watch?v=aAkurCTifE0</strong>")
    logomarca = models.ImageField("Imagem", upload_to='uploads/galerias/', max_length=100)
    # logomarca = ImageWithThumbnailsField(
    #     upload_to='uploads/clientes/',
    #     thumbnail={
    #         'size': (120, 80),
    #         'options': ('pad', )
    #     },
    #     extra_thumbnails={
    #         'detalhes': {
    #             'size': (270, 210),
    #             'options': ('pad',)
    #         },
    #         'big': {
    #             'size': (500, 500),
    #             'options': ('pad',)
    #         },
    #     }
    # )
    
    # Generic ForeignKey
    imagens = generic.GenericRelation(Imagem)
   	#anexos = generic.GenericRelation(Anexo)
    
    def get_absolute_url(self):
        return "/clientes/%i/%s" % (self.id, self.slug)
    
    # Retorna o primeiro paragrafo da descrição do Cliente
    def primeiro_paragrafo(self):
        """Retorna o Primeiro Paragrafo da descrição do Cliente"""
        primeiro_paragrafo = list(self.descricao.partition('</p>'))
        return ''.join([primeiro_paragrafo[0], primeiro_paragrafo[1]])
    
    def __unicode__(self):
        return self.nome
    
    # Método customizado para salvar o SLUG
    def save(self):
        self.slug = slugify(self.nome)
        super(Cliente, self).save()
    
    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = "Clientes"
        
class Banner(models.Model):
    nome = models.CharField("Nome do Banner", max_length=200)
    descricao = models.CharField(u"Descrição", max_length=300)
    banner = models.FileField("Banner", upload_to='uploads/banners/', max_length=100, help_text="Proporção: largura = 965px e altura = 164px. (Formato: PNG, Jpeg ou Flash)")
    pagina = models.CharField(choices=settings.PAGINAS_CHOICES, max_length=200)
    principal = models.BooleanField(default=False, verbose_name="Banner Principal", help_text="Este banner aparecerá em todas as páginas as quais não forem atribuídos um banner específico. Você poderá marcar apenas um banner como principal.")
    
    def __unicode__(self):
        return self.nome
    
    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = "Banners"


class Pagina(models.Model):
    titulo = models.CharField("Título da Página", max_length=200)
    conteudo = models.TextField(u"Conteúdo da Página")
    titulo_galeria = models.CharField("Título da Galeria de Imagens", blank=True, max_length=200, help_text="Digite um nome para a Galeria de Imagens, deixe o campo em branco caso queira manter o nome como Galeria de Imagens.")
    video = models.CharField("Vídeo do YouTube", max_length=150, blank=True, help_text="Digite a URL do vídeo seguindo este exemplo: <strong>http://www.youtube.com/watch?v=aAkurCTifE0</strong>")
    video_key = models.CharField(blank=True, max_length=255, editable=False)
    
    # Generic ForeignKey
    imagens = generic.GenericRelation(Imagem)
   # anexos = generic.GenericRelation(Anexo)
    
    # Estatisticas
    visitas = models.IntegerField(default=0, editable=False)
    
    def __unicode__(self):
        return self.titulo
    
    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = u"Páginas"

class Imagens(models.Model):
    nome = models.CharField("Nome do Banner", max_length=200)
    descricao = models.CharField(u"Descrição", max_length=300)
    caminho = models.CharField(u"caminho", max_length=300, default="media/images/slidshow/")
    
    def __unicode__(self):
        return self.nome
    
    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = "Imagens"



class Configuracao(models.Model):
    chave = models.CharField(max_length=255)
    valor = models.TextField(blank=True)
    
    @staticmethod
    def recupera_dicionario():
        """ Função que retorna as configurações do sistema em um dicionario """
        configuracoes = dict()
        for x in Configuracao.objects.all():
            configuracoes[x.chave] = x.valor

        return configuracoes
    
    def __unicode__(self):
        return self.chave
    
    # Alterando o nome pluralizado da classe
    class Meta:
        verbose_name_plural = u"Configurações"

class Imagens(models.Model):
     imagem = models.ImageField("Imagens", upload_to='media/images/slidshow', max_length=100)
    #imagem = ImageWithThumbnailsField(
        #upload_to='/media/images/slidshow',
        #thumbnail={
         #   'size': (270, 210),
          #  'options': ('pad',)
	    #}
