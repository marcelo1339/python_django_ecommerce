from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
# Create your views here.

class ListaProdutos(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Listar')


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