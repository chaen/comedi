# -*- coding: utf8 -*-

from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from models import Family, SubFamily, Unit, UnitConversion, Tva, \
                   Product, Order, OrderItem, City, Client, Seller, Period, UsualComment

admin.site.register( Family )
admin.site.register( SubFamily )
admin.site.register( Unit )
admin.site.register( UnitConversion )
admin.site.register( Tva )
admin.site.register( City )
admin.site.register( Client )
admin.site.register( Seller )
admin.site.register( Period )
admin.site.register( UsualComment )

class UnitConversionInline( admin.StackedInline ):
  model = UnitConversion
  extra = 1

class ProductAdmin( admin.ModelAdmin ):
  inlines = [UnitConversionInline]
  list_display = ('name',)
admin.site.register( Product, ProductAdmin )



class OrderItemInline( admin.TabularInline ):
  model = OrderItem
  extra = 1

class OrderAdmin( admin.ModelAdmin ):
  inlines = [OrderItemInline]

admin.site.register( Order, OrderAdmin )




# from django import forms
#
# from django_options.admin import OptionsPage, admin_pages, option
# from django_options.forms import OptionsForm
#
# class GeneralsAdminPage( OptionsPage ):
#
#   title = "General options"
#   description = "Very important options"
#   code = 'generals'
#
#
#   class SiteInfoForm( OptionsForm ):
#
#     code = 'site_info'
#     title = 'Site information'
#     description = 'Small description of this form'
#
#     # options
#     site_title = option( forms.CharField( max_length = 255 ) )
#     site_description = option( forms.CharField( widget = forms.Textarea ) )
#
# admin_pages.register( GeneralsAdminPage )
