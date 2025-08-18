from django.contrib import admin
from . import models

# Register your models here.


class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1

@admin.register(models.ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = (ItemPedidoInline,)