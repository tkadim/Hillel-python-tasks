import stripe
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from base import settings
from cart.cart import get_cart
from .models import Order
from .services import create_order_from_cart, validate_payment
import logging

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = get_cart(request)
    items = cart.get_items()

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

        if order is None:
            return redirect('cart:cart_detail')

        return redirect('orders:order_detail', order_id=order.id)

    context = {
        "items": items,
        "total_price": cart.total_price,
        "total_items": cart.total_items,
    }

    return render(request, 'orders/checkout.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def create_checkout_session(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != Order.Status.PENDING:
        return redirect("orders:order_detail", order_id=order.id)

    line_items = []
    for item in order.items.all():
        line_items.append({
            "price_data": {
                "currency": "uah",
                "product_data": {
                    "name": item.book_title,
                },
                "unit_amount": int(item.price_at_purchase * 100),
            },
            "quantity": item.quantity,
        })

    checkout_session = stripe.checkout.Session.create(
        # payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("orders:payment_success", kwargs={"order_id": order.id})
        ) + "?session_id={CHECKOUT_SESSION_ID}",

        cancel_url=request.build_absolute_uri(
            reverse("orders:payment_cancel", kwargs={"order_id": order.id})
        ),

        metadata={"order_id": str(order.id)},
        customer_email=request.user.email,
    )

    order.stripe_checkout_session_id = checkout_session.id
    order.save(update_fields=["stripe_checkout_session_id"])

    # Редірект на хостовану Stripe-сторінку оплати
    return redirect(checkout_session.url, permanent=False)


@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/payment_success.html", {"order": order})


@login_required
def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/payment_cancel.html", {"order": order})


def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError:
        return HttpResponseBadRequest("Invalid signature")

    if event.type == "checkout.session.completed":

        session = event.data.object
        order_id = session.metadata['order_id']

        if order_id:
            with transaction.atomic():
                order = Order.objects.get(id=order_id)
                validate_payment(order, event)
                order.status = Order.Status.PAID
                order.stripe_payment_intent_id = session.get("payment_intent", "")
                order.save(update_fields=["status", "stripe_payment_intent_id"])
                #send email

    return HttpResponse(status=200)