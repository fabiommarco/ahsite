from app.models import *
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
# from django.contrib.contenttypes import GenericTabularInline, generic_inlineformset_factor
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.utils.safestring import mark_safe

ImagemGenericFormSet = generic_inlineformset_factory(Imagem, extra=1)
AttachGenericFormSet = generic_inlineformset_factory(Attachment, extra=1)


class ImagemInline(GenericTabularInline):
    model = Imagem
    extra = 1
    ct_field_name = "content_type"
    id_field_name = "object_id"


class AttachInline(GenericTabularInline):
    model = Attachment
    extra = 1
    ct_field_name = "content_type"
    id_field_name = "object_id"


class EventAdmin(admin.ModelAdmin):
    list_display = ("event_title", "language")
    inlines = [ImagemInline, AttachInline]


class NewsAdmin(admin.ModelAdmin):
    list_display = ("news_title", "language")
    inlines = [ImagemInline, AttachInline]


class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        "news_date",
        "news_name",
        "news_email",
    )
    ordering = ["news_date"]


class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = (
        "scaped_html",
        "language",
    )
    inlines = [ImagemInline, AttachInline]


class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "language", "parent", "sale_email", "preview_content", "created_at")
    list_filter = ("language", "parent")
    search_fields = ("sale_description", "sale_email")
    readonly_fields = ("id",)
    list_per_page = 10
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('language', 'parent', 'sale_email'),
            'classes': ('wide',)
        }),
        ('Conteúdo da Página', {
            'fields': ('sale_description',),
            'description': 'Conteúdo principal da página de compras. Use o editor para formatar o texto.',
            'classes': ('wide',)
        }),
    )
    
    def created_at(self, obj):
        """Campo calculado para mostrar quando foi criado"""
        return f"ID: {obj.id}"
    created_at.short_description = 'ID'
    
    def preview_content(self, obj):
        """Mostra uma prévia do conteúdo"""
        content = obj.sale_description
        if len(content) > 100:
            return f"{content[:100]}..."
        return content
    preview_content.short_description = "Prévia do Conteúdo"
    
    def get_queryset(self, request):
        """Ordena por ID para mostrar os mais recentes primeiro"""
        return super().get_queryset(request).order_by('-id')


class ResearchAdmin(admin.ModelAdmin):
    list_display = ("reserach_date", "reserach_title", "reserach_type", "research_file")


class ProdAdmin(admin.ModelAdmin):
    list_display = ("product_name", "product_category", "language")
    inlines = [ImagemInline, AttachInline]


class EnvAdmin(admin.ModelAdmin):
    list_display = ("environ_title", "language")
    inlines = [ImagemInline, AttachInline]


class PartnersAdmin(admin.ModelAdmin):
    list_display = ("partner_title", "language")


class FarmAdmin(admin.ModelAdmin):
    list_display = (
        "farm_name",
        "farm_latitude",
        "farm_longitude",
        "farm_city",
        "farm_state",
    )


class TimeLineAdmin(admin.ModelAdmin):
    list_display = ("year", "short_description")


class EquipeComprasAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "telefone_completo", "cargo", "local", "ativo", "ordem", "data_criacao")
    list_filter = ("ativo", "local", "cargo", "data_criacao")
    search_fields = ("nome", "email", "cargo", "local")
    list_editable = ("ativo", "ordem")
    ordering = ("ordem", "nome")
    list_per_page = 20
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email', 'cargo'),
            'classes': ('wide',)
        }),
        ('Contato', {
            'fields': ('telefone', 'ramal'),
            'classes': ('wide',)
        }),
        ('Localização', {
            'fields': ('local',),
            'classes': ('wide',)
        }),
        ('Configurações', {
            'fields': ('ativo', 'ordem'),
            'description': 'Controle se o membro está ativo e a ordem de exibição na lista.',
            'classes': ('wide',)
        }),
    )
    
    readonly_fields = ('data_criacao', 'data_atualizacao')
    
    actions = ['ativar_membros', 'desativar_membros', 'reordenar_membros']
    
    def telefone_completo(self, obj):
        return obj.telefone_completo()
    telefone_completo.short_description = "Telefone"
    
    def ativar_membros(self, request, queryset):
        updated = queryset.update(ativo=True)
        self.message_user(request, f'{updated} membro(s) ativado(s) com sucesso.')
    ativar_membros.short_description = "Ativar membros selecionados"
    
    def desativar_membros(self, request, queryset):
        updated = queryset.update(ativo=False)
        self.message_user(request, f'{updated} membro(s) desativado(s) com sucesso.')
    desativar_membros.short_description = "Desativar membros selecionados"
    
    def reordenar_membros(self, request, queryset):
        for i, membro in enumerate(queryset.order_by('ordem', 'nome'), 1):
            membro.ordem = i
            membro.save()
        self.message_user(request, f'Ordem de {queryset.count()} membro(s) atualizada.')
    reordenar_membros.short_description = "Reordenar membros selecionados"


class BannerAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ativo", "ordem", "data_criacao", "preview_imagem")
    list_filter = ("ativo", "data_criacao")
    search_fields = ("titulo", "descricao")
    list_editable = ("ativo", "ordem")
    ordering = ("ordem", "data_criacao")
    list_per_page = 20
    date_hierarchy = 'data_criacao'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'link'),
            'classes': ('wide',)
        }),
        ('Imagem', {
            'fields': ('imagem',),
            'description': 'Recomendado: 1920x600px para melhor visualização.',
            'classes': ('wide',)
        }),
        ('Configurações', {
            'fields': ('ativo', 'ordem'),
            'description': 'Controle se o banner está ativo e a ordem de exibição.',
            'classes': ('wide',)
        }),
    )
    
    readonly_fields = ('data_criacao', 'data_atualizacao')
    
    actions = ['ativar_banners', 'desativar_banners', 'reordenar_banners']
    
    def preview_imagem(self, obj):
        if obj.imagem:
            return mark_safe(f'<img src="{obj.imagem.url}" style="max-height: 50px; max-width: 100px; object-fit: cover;" />')
        return "-"
    preview_imagem.short_description = "Prévia"
    
    def ativar_banners(self, request, queryset):
        updated = queryset.update(ativo=True)
        self.message_user(request, f'{updated} banner(s) ativado(s) com sucesso.')
    ativar_banners.short_description = "Ativar banners selecionados"
    
    def desativar_banners(self, request, queryset):
        updated = queryset.update(ativo=False)
        self.message_user(request, f'{updated} banner(s) desativado(s) com sucesso.')
    desativar_banners.short_description = "Desativar banners selecionados"
    
    def reordenar_banners(self, request, queryset):
        for i, banner in enumerate(queryset.order_by('ordem', 'data_criacao'), 1):
            banner.ordem = i
            banner.save()
        self.message_user(request, f'Ordem de {queryset.count()} banner(s) atualizada.')
    reordenar_banners.short_description = "Reordenar banners selecionados"


admin.site.register(Products, ProdAdmin)
admin.site.register(Jobs)
admin.site.register(EnvironmentalResponsability, EnvAdmin)
admin.site.register(Partners, PartnersAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Magazine)
admin.site.register(AboutCompany, AboutCompanyAdmin)
admin.site.register(GeneralConfig)
admin.site.register(Event, EventAdmin)
admin.site.register(AgriculturalFiles)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Farm, FarmAdmin)
admin.site.register(TimeLine, TimeLineAdmin)
admin.site.register(EquipeCompras, EquipeComprasAdmin)
admin.site.register(Banner, BannerAdmin)
