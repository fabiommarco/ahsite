from django.contrib import admin
from app.models import *
# from django.contrib.contenttypes import GenericTabularInline, generic_inlineformset_factor
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.contrib.contenttypes.admin import GenericTabularInline
ImagemGenericFormSet = generic_inlineformset_factory(Imagem, extra=1)


class ImagemInlineFormset(ImagemGenericFormSet):
    def clean(self):
        principal_count = 0

        for form in self.forms:
            try:
                if form.cleaned_data:
                    if form.cleaned_data["main_image"] == True:
                        principal_count += 1
            except:
                pass

        if principal_count > 1:
            raise forms.ValidationError("Selecione apenas uma imagem como Principal.")

class ImagemInline(GenericTabularInline):
    formset = ImagemInlineFormset
    model = Imagem
    extra = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class EventAdmin(admin.ModelAdmin):
    # list_display = ('scaped_html', )
    inlines = [ImagemInline]

class NewsAdmin(admin.ModelAdmin):
    # list_display = ('scaped_html', )
    inlines = [ImagemInline]

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('news_date','news_name','news_email',)
    ordering = ['news_date']

class AboutCompanyAdmin(admin.ModelAdmin):
    list_display = ('scaped_html', )
    inlines = [ImagemInline]


class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_email', )

class ProdAdmin(admin.ModelAdmin):
    inlines = [ImagemInline]

class EnvAdmin(admin.ModelAdmin):
    inlines = [ImagemInline]
    
admin.site.register(Products, ProdAdmin)
admin.site.register(Jobs)
admin.site.register(EnvironmentalResponsability,EnvAdmin)
admin.site.register(Partners)
admin.site.register(Sale, SaleAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Newsletter,NewsletterAdmin)
admin.site.register(Magazine)
admin.site.register(AboutCompany,AboutCompanyAdmin)
admin.site.register(GeneralConfig)
admin.site.register(Event,EventAdmin)
admin.site.register(AgriculturalFiles)


