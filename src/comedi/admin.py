from django.contrib import admin

# Register your models here.
from comedi.models import Family, SubFamily, Unit, UnitConversion, Tva, Product, Order, OrderItem
admin.site.register( Family )
admin.site.register( SubFamily )
admin.site.register( Unit )
admin.site.register( UnitConversion )
admin.site.register( Tva )

class UnitConversionInline( admin.StackedInline ):
  model = UnitConversion
  extra = 1

class ProductAdmin( admin.ModelAdmin ):
  inlines = [UnitConversionInline]

admin.site.register( Product, ProductAdmin )



class OrderItemInline( admin.StackedInline ):
  model = OrderItem
  extra = 1

class OrderAdmin( admin.ModelAdmin ):
  inlines = [OrderItemInline]

admin.site.register( Order, OrderAdmin )
