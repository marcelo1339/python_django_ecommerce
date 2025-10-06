def format_brazilian_currency(value):
    return f'R$ {value:.2f}'.replace('.', ',')

def total_qtd_cart(cart):
    return sum([item['quantidade'] for item in cart.values()])