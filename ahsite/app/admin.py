from django.contrib import admin
from app.models import *
# from django.contrib.contenttypes import GenericTabularInline, generic_inlineformset_factor
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.admin import GenericTabularInline

ImagemGenericFormSet = generic_inlineformset_factory(Imagem, extra=1)
AttachGenericFormSet = generic_inlineformset_factory(Attachment, extra=1)


class ImagemInline(GenericTabularInline):
    model = Imagem
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class AttachInline(GenericTabularInline):
    model = Attachment
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'language')
    inlines = [ImagemInline, AttachInline]

class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'language')
    inlines = [ImagemInline, AttachInline]

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('news_date','news_name','news_email',)
    ordering = ['news_date']

class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = ('scaped_html','language',)
    inlines = [ImagemInline, AttachInline]

class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_email', 'language')

class ResearchAdmin(admin.ModelAdmin):
    list_display = ('reserach_date','reserach_title', 'reserach_type', 'research_file' )

class ProdAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'language')
    inlines = [ImagemInline, AttachInline]

class EnvAdmin(admin.ModelAdmin):
    list_display = ('environ_title', 'language')
    inlines = [ImagemInline, AttachInline]

class PartnersAdmin(admin.ModelAdmin):
    list_display = ('partner_title', 'language')

admin.site.register(Products, ProdAdmin)
admin.site.register(Jobs)
admin.site.register(EnvironmentalResponsability,EnvAdmin)
admin.site.register(Partners, PartnersAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Newsletter,NewsletterAdmin)
admin.site.register(Magazine)
admin.site.register(AboutCompany,AboutCompanyAdmin)
admin.site.register(GeneralConfig)
admin.site.register(Event,EventAdmin)
admin.site.register(AgriculturalFiles)
admin.site.register(Research,ResearchAdmin)



