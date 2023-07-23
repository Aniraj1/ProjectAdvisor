from django.contrib import admin
from .models import Order,UserSubscription

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','price','user','created_at','payment_status','payment_mode']
    list_filter = ['price', 'user', 'created_at','payment_status','payment_mode']
    
@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display=['can_order','user']
    list_filter= ["can_order",]
    
# admin.site.register("Order")