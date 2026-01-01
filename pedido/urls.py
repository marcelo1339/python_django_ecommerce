from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/<int:pk>', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvar_pedido'),
    path('detalhe/', views.Detalhe.as_view(), name='detalhe'),
    path('lista/', views.ListaPedidos.as_view(), name='lista'),
]
