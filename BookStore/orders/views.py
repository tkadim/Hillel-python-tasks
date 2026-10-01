from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .services import create_order_from_cart
import logging

logger = logging.getLogger(__name__)

@login_required
def checkout(request):
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '')
        phone_number = request.POST.get('phone_number', '')

        try:
            order = create_order_from_cart(
                request,
                shipping_address=shipping_address,
                phone_number=phone_number,
            )
        except ValidationError as e:
            logger.error(request, str(e))
            return redirect("cart:cart_detail")

        if order in None:
            return redirect('cart:cart_detail')

        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html')


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})