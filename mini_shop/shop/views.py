from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


from django.shortcuts import redirect
from .models import Cart

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_id = request.session.session_key

    if not session_id:
        request.session.create()

    cart_item, created = Cart.objects.get_or_create(session_id=session_id, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


def cart_view(request):
    session_id = request.session.session_key
    cart_items = Cart.objects.filter(session_id=session_id)
    total = sum(item.total_price() for item in cart_items)
    
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('cart_view')
