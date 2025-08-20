from django.contrib import admin
from . import models
# Register your models here.


class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1

@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    inlines = (VariacaoInline,)
    list_display = ('nome', 'descricao_curta', 'get_preco_formatado', 'get_preco_promocional_formatado')

@admin.register(models.Variacao)
class VariacaoAdmin(admin.ModelAdmin):
    ...