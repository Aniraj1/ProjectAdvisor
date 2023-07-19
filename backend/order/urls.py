from django.urls import path
from . import views

urlpatterns = [
    path("webhook/",views.stripe_webhook,name="webhook"),
    path("get-all/",views.get_order,name = "get-all-orders"),
    path("<int:pk>/get-single-order/",views.get_single_order,name="get-single-order"),
    path("add-new/",views.add_order,name = "add-new-order"),
    path("<int:pk>/update/",views.process_order,name ="update-order"),
    path("<int:pk>/delete/",views.delete_order,name="delete-order"),
    path("create-checkout-session/",views.create_checkout_session,name= "create-checkout-session"),
    path("customer-portal/",views.customer_portal,name="customer-portal"),

]
