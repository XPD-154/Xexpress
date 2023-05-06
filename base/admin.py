from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
  list_display = ("name", "email",)
admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
  list_display = ("name", "price", "digital", "image",)
admin.site.register(Product, ProductAdmin)

class OrderAdmin(admin.ModelAdmin):
  list_display = ("date_ordered", "complete", "transaction_id", "customer_id",)
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
  list_display = ("quantity", "date_added", "order_id", "product_id",)
admin.site.register(OrderItem, OrderItemAdmin)

class ShippingAddressAdmin(admin.ModelAdmin):
  list_display = ("address", "city", "state", "zipcode", "date_added", "customer_id", "order_id",)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
