from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("checkout/", views.checkout, name="checkout"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("<int:order_id>/pay/", views.create_checkout_session, name="create_checkout_session"),
    path("<int:order_id>/payment-success/", views.payment_success, name="payment_success"),
    path("<int:order_id>/payment-cancel/", views.payment_cancel, name="payment_cancel"),
]