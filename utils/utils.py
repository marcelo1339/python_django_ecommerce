def format_brazilian_currency(value):
    return f'R$ {value:.2f}'.replace('.', ',')

def total_qtd_cart(cart):
    return sum([item['quantidade'] for item in cart.values()])

def calculate_price_quantitative(cart):
    for product in cart.values():
        product['preco_quantitativo_promocional'] = product['quantidade'] * product['preco_unitario_promocional']
        product['preco_quantitativo'] = product['quantidade'] * product['preco_unitario']

def cart_totals(cart):
    
    total = 0
    for product in cart.values():
        if product['preco_quantitativo_promocional'] > 0:
            total += product['preco_quantitativo_promocional']
            continue
        if product['preco_quantitativo'] > 0:
            total += product['preco_quantitativo']
    
    return total