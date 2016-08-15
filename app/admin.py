#-*- coding: utf-8 -*-
import datetime
from app.models import Noticia, Imagem, Anexo, Banner, Configuracao, \
                                Pagina
                                
from django import forms
from django.contrib import admin
from django.conf import settings
from django.forms.util import ErrorList
from django.contrib.contenttypes.generic import GenericTabularInline, generic_inlineformset_factory

ImagemGenericFormSet = generic_inlineformset_factory(Imagem, extra=1)
AnexoGenericFormSet = generic_inlineformset_factory(Anexo, extra=1)

class ImagemInlineFormset(ImagemGenericFormSet):
    def clean(self):
        max_count = 0
        principal_count = 0
        
        class_name = self.instance.__class__.__name__
        
        for form in self.forms:
            try:
                if form.cleaned_data:
                    max_count += 1
                    
                    if form.cleaned_data["imagem_principal"] == True:
                        principal_count += 1
            except:
                pass
        
        if max_count > settings.MAX[class_name]["ImagemInline"]:
            raise forms.ValidationError("Máximo de imagens atingido.")
            
        if principal_count > 1:
            raise forms.ValidationError("Selecione apenas uma imagem como Principal.")
            
class AnexoInlineFormset(AnexoGenericFormSet):
    def clean(self):
        count = 0

        class_name = self.instance.__class__.__name__

        for form in self.forms:
            if form.cleaned_data:
                count += 1

        if count > settings.MAX[class_name]["AnexoInline"]:
            raise forms.ValidationError("Máximo de anexos atingido.")

class ImagemInline(GenericTabularInline):
    formset = ImagemInlineFormset
    model = Imagem
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'
    
class AnexoInline(GenericTabularInline):
    formset = AnexoInlineFormset
    model = Anexo
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data')
    inlines = [ImagemInline, AnexoInline]
    
    # TinyMCE
    class Media:
        js = ['/media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/media/admin/tinymce_setup/tinymce_setup.js',]
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao_short', 'logomarca')
    inlines = [ImagemInline, AnexoInline]
    
    def descricao_short(self, cliente):
        return cliente.primeiro_paragrafo()
    descricao_short.allow_tags = True
    
    # TinyMCE
    class Media:
        js = ['/media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/media/admin/tinymce_setup/tinymce_setup.js',]

class ProdutoAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProdutoAdminForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].choices = categorias_choices()
    
def categorias_choices():
    categorias = []
    for categoria in CategoriaProduto.objects.filter(categoria_pai=None):
        nova_categoria = []
        sub_categorias = []
        for sub_categoria in CategoriaProduto.objects.filter(categoria_pai=categoria):
            sub_categorias.append([sub_categoria.id, sub_categoria.nome])
        
        if len(sub_categorias) > 0:
            nova_categoria = [categoria.nome, sub_categorias]
        else:
            nova_categoria = [categoria.id, categoria.nome]
            
        categorias.append(nova_categoria)

    return categorias

    
    class Meta:
        model = Produto

class ProdutoAdmin(admin.ModelAdmin):
    form = ProdutoAdminForm
    list_display = ('nome', 'descricao_short', 'categoria', 'destaque')
    inlines = [ImagemInline, AnexoInline]
    actions = ['marca_destaque']
    
    def descricao_short(self, produto):
        return produto.primeiro_paragrafo()
    descricao_short.allow_tags = True
    
    
    # Action: Marca como destaque
    def marca_destaque(self, request, queryset):
        for item in queryset:
            # Alterando o status do resumo
            item.destaque = True

            # Salvando as Alterações
            item.save()

        # Mostrando mensagem na tela
        self.message_user(request, "%s produto(s) foram marcados com sucesso!" % queryset.count())

    marca_destaque.short_description = u'Marcar Produtos selecionados como Destaque'
    
    # TinyMCE
    class Media:
        js = ['/media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/media/admin/tinymce_setup/tinymce_setup.js',]
        
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao_short', 'destaque')
    inlines = [ImagemInline, AnexoInline]
    actions = ['marca_destaque']

    def descricao_short(self, servico):
        return servico.primeiro_paragrafo()
    descricao_short.allow_tags = True

    # Action: Marca como destaque
    def marca_destaque(self, request, queryset):
        for item in queryset:
            # Alterando o status do resumo
            item.destaque = True

            # Salvando as Alterações
            item.save()

            # Mostrando mensagem na tela
            self.message_user(request, "%s serviço(s) foram marcados com sucesso!" % queryset.count())

    marca_destaque.short_description = u'Marcar Serviços selecionados como Destaque'

    # TinyMCE
    class Media:
        js = ['/media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/media/admin/tinymce_setup/tinymce_setup.js',]

class BannerForm(forms.ModelForm):
    def clean_principal(self):
        principal = self.cleaned_data["principal"]
        
        # Validando o campo Principal, pode existir apenas um
        if principal and len(Banner.objects.filter(principal=True).exclude(id=self.instance.id)) > 0:
            raise forms.ValidationError(u'Um banner já foi marcado como principal anteriormente. Por favor, desmarque o banner anterior para então poder marcar este.')
        
        return principal
        
    def clean_banner(self):
        banner = self.files.get("banner")
        if self.files.get("banner"):
            if banner.content_type in ["image/jpeg", "image/png"]:
                from PIL import Image
                banner_size = Image.open(banner).size
                
                if banner_size[0] <> 965 or banner_size[1] <> 164:
                    raise forms.ValidationError(u'Por favor, salve o banner na proporção: largura = 965px e altura = 164px.')
            elif banner.content_type == "application/x-shockwave-flash":
                pass
            else:
                raise forms.ValidationError(u'O banner deve estar em um dos seguintes formatos: PNG, Jpeg ou Flash (swf).')
        return banner
    
    def clean_pagina(self):
        pagina = self.cleaned_data["pagina"]
        
        # Validando a página, apenas um banner por pagina
        banners = Banner.objects.filter(pagina=pagina).exclude(id=self.instance.id)
        if len(banners) > 0:
            raise forms.ValidationError(u'Um banner já foi escolhido para esta página anteriormente.')
        
        return pagina
    
    class Meta:
        model = Banner

class BannerAdmin(admin.ModelAdmin):
    form = BannerForm
    list_display = ('nome', 'banner', 'pagina', 'principal')
    
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'data')

class PaginaAdmin(admin.ModelAdmin):
    inlines = [ImagemInline, AnexoInline]
    # TinyMCE
    class Media:
        js = ['/media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/media/admin/tinymce_setup/tinymce_setup.js',]
        
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('chave', 'valor')
admin.site.register(Configuracao, ConfiguracaoAdmin)


admin.site.register(Pagina, PaginaAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Banner, BannerAdmin)


#########################
#### Unregisters ########
try:
    from django_evolution.models import Version, Evolution
    admin.autodiscover()
    admin.site.unregister(Version)
    admin.site.unregister(Evolution)
except:
    pass
