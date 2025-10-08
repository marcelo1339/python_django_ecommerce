from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from . import models
from utils import utils


# Create your views here.

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
    


class AdicionarCarrinho(View):
    def get(self, *args, **kwargs):
  
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )

        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não existe')
            return redirect(http_referer)

        variacao = get_object_or_404(models.Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque

        produto = variacao.produto
        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem
        if imagem:
            imagem = imagem.name
        else:
            imagem = ''
        
        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)


        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no produto "{produto_nome}".'
                    f'\nAdicionamos {variacao_estoque}x ao seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * quantidade_carrinho

        else:
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem,
            }

        self.request.session.save()   
        
        messages.success(
            self.request,
            f'Produto {produto_nome} {variacao_nome} adicionado ao seu carrinho'
            f' {carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)

class RemoverCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )

        del_prod_slug = self.request.GET.get('slug')
        del_prod_variacao = self.request.GET.get('vid')

        if not del_prod_variacao or \
        not self.request.session.get('carrinho') or \
        del_prod_variacao not in self.request.session['carrinho'].keys():
            return redirect(http_referer)

       
        qtd_item = self.request.session['carrinho'][del_prod_variacao]['quantidade']
        if qtd_item <= 1:
            del self.request.session['carrinho'][f'{del_prod_variacao}']
        else:
            self.request.session['carrinho'][f'{del_prod_variacao}']['quantidade'] -= 1

        carrinho = self.request.session['carrinho']
        utils.calculate_price_quantitative(carrinho)

        self.request.session.save()

        del_variacao_nome = get_object_or_404(models.Variacao, pk=del_prod_variacao).nome
        messages.success(
            self.request,
            f'Produto: "{del_prod_slug}" - Variação: "{del_variacao_nome}" removido com sucesso!'
        )

        return redirect('produto:carrinho')



class Carrinho(View):
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        
        return render(
            self.request,
            'produto/carrinho.html',
            context=contexto,
        )

class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')