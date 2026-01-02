from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse

from .models import Pedido, ItemPedido
from produto.models import Variacao
from utils.utils import calculate_price_quantitative, cart_totals, total_qtd_cart

# Create your views here.

class DispatchLoginRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(request, *args, **kwargs)


class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    def get_queryset(self, *args, **kwargs):
    
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)

        return qs
    

    

class SalvarPedido(View):
    
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('perfil:criar')
        
        carrinho = self.request.session.get('carrinho')
        
        if not carrinho:
            messages.error(
                self.request,
                'Carrinho está vazio.'
            )
            return redirect('produto:lista')

        id_variacoes_carrinho = [ vid for vid in carrinho.keys() ]
        
        variacoes_banco = list(
            Variacao.objects.select_related('produto').filter(id__in=id_variacoes_carrinho)
        )

        msg_estoque_insuficiente = ''

        for variacao in variacoes_banco:
            vid = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho=carrinho[vid]['quantidade']

            if qtd_carrinho > estoque:
                carrinho[vid]['quantidade'] = estoque
                msg_estoque_insuficiente = 'Estoque insuficiente para 1 ou mais produtos. Quantidade ajustada.'

        calculate_price_quantitative(carrinho)
        self.request.session.save()

        if msg_estoque_insuficiente:
            messages.error(
                self.request,
                msg_estoque_insuficiente
            )

            return redirect('produto:carrinho')
        
        qtd_total_carrinho = total_qtd_cart(carrinho)
        total_valor_carrinho = cart_totals(carrinho)

        pedido = Pedido(
            usuario = self.request.user,
            total = total_valor_carrinho,
            qtd_total = qtd_total_carrinho,
            status = 'C'
        )
        pedido.save()

       
        ItemPedido.objects.bulk_create(
            [ 
                ItemPedido(
                    pedido=pedido,
                    produto=v_details['produto_nome'],
                    produto_id=v_details['produto_id'],
                    variacao=v_details['variacao_nome'],
                    variacao_id=v_details['variacao_id'],
                    preco=v_details['preco_unitario'],
                    preco_promocional=v_details['preco_unitario_promocional'],
                    quantidade=v_details['quantidade'],
                    imagem=v_details['imagem']
                )
                for v_details in carrinho.values() 
            ]
        )

        del self.request.session['carrinho']

        return redirect(
            reverse('pedido:pagar', kwargs={'pk':pedido.id})
        )
    

class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'


class ListaPedidos(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = '-id',

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(usuario = self.request.user)

        return qs    