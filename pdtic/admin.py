from django.contrib import admin
from .models import PDTIC, VersaoPDTIC

class VersaoInline(admin.TabularInline):
    model = VersaoPDTIC
    extra = 1

@admin.register(PDTIC)
class PDTICAdmin(admin.ModelAdmin):
    list_display = ("titulo", "instituicao", "vigencia_inicio", "vigencia_fim", "status")
    list_filter = ("status", "instituicao")
    search_fields = ("titulo", "instituicao__nome")
    inlines = [VersaoInline]


@admin.register(VersaoPDTIC)
class VersaoPDTICAdmin(admin.ModelAdmin):
    list_display = ("pdtic", "numero_versao", "data_aprovacao")
    list_filter = ("pdtic",)
    search_fields = ("numero_versao", "pdtic__titulo")