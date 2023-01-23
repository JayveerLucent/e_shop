from django import template

register = template.Library()

@register.filter(name = 'is_in_cart')
def is_in_cart(product , cart):
    print("Pro and car---- ",product , cart)
    keys = cart.keys()
    print("hi-----c",keys)
    for id in keys:
        if id is None:
            return False
        elif int(id) == product.id:
            return True
    print(product, cart)
    return False

@register.filter(name = 'cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
        
    print(product, cart.get(id))
    return 0

@register.filter(name = 'price_total')
def price_total(product, cart):
    return product.price * cart_quantity(product,cart)

@register.filter(name = 'final_price')
def final_price(products, cart):
    sum=0
    for p in products:
        sum+= price_total(p, cart)
    return sum