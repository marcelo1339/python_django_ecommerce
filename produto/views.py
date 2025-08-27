from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from . import models
# Create your views here.

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10


class DetalheProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe')


class AdicionarCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AdicionarCarrinho')

class RemoverCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover Carrinho')


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')

class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')