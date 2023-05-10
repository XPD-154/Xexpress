from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# Register your models here.

#determine columns displayed in admin panel for the model registered below
class CustomerAdmin(admin.ModelAdmin):
  list_display = ("name", "email",)
#register the model to show it in admin panel and attach the class above
admin.site.register(Customer, CustomerAdmin)

#determine columns displayed in admin panel for the model registered below
class ProductAdmin(admin.ModelAdmin):
  list_display = ("name", "price", "digital", "image",)
#register the model to show it in admin panel and attach the class above
admin.site.register(Product, ProductAdmin)

#determine columns displayed in admin panel for the model registered below
class OrderAdmin(admin.ModelAdmin):
  list_display = ("date_ordered", "complete", "transaction_id", "customer_id",)
#register the model to show it in admin panel and attach the class above
admin.site.register(Order, OrderAdmin)

#determine columns displayed in admin panel for the model registered below
class OrderItemAdmin(admin.ModelAdmin):
  list_display = ("quantity", "date_added", "order_id", "product_id",)
#register the model to show it in admin panel and attach the class above
admin.site.register(OrderItem, OrderItemAdmin)

#determine columns displayed in admin panel for the model registered below
class ShippingAddressAdmin(admin.ModelAdmin):
  list_display = ("address", "city", "state", "zipcode", "date_added", "customer_id", "order_id",)
#register the model to show it in admin panel and attach the class above
admin.site.register(ShippingAddress, ShippingAddressAdmin)
