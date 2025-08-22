from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('adicionarcarrinho/', views.AdicionarCarrinho.as_view(), name='adicionar_carrinho'),
    path('removercarrinho/', views.RemoverCarrinho.as_view(), name='remover_carrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('finalizar/', views.Finalizar.as_view(), name='finalizar'),
    path('<slug>/', views.DetalheProduto.as_view(), name='detalhe'),
]
