from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagar')

class Fechar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Fechar')
    

class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe Pedido')
    