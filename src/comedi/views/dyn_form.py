from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import ModelForm
from django import forms
from comedi.models import Product, Family, SubFamily
from django.shortcuts import render_to_response
import datetime
from django.contrib.admin.widgets import AdminDateWidget

import json


# <script>
#     $("#id_subFamily").change(function() {
#       var subfamily = $(this).val();
#       alert( subfamily.concat(" Handler for .change() called.")  );
#     });
# </script>


# <script>
# $("#id_family").change(function() {
#     var family = $(this).val();
#     $.getJSON("{% url 'list_subfamilies' %}", { family: family }, function(id_subFamily) {
#         var id_subFamily_select = $("#id_subFamily");
#     });
# });
# </script>

def ajax_getSubFamilyNamesFromFamily( request ):
  subFamilies = dict( ( sf.id , sf.name ) for sf in SubFamily.objects.filter( family__pk = request.GET["family"] ) )
  try:
    ret = json.dumps( subFamilies )
  except Exception, e:
    print e
  return HttpResponse( ret )

def ajax_getProductNamesFromSubFamily( request ):
  products = dict( ( p.id , p.name ) for p in Product.objects.filter( subFamily__pk = request.GET["subFamily"] ) )
  try:
    ret = json.dumps( products )
  except Exception, e:
    print e
  return HttpResponse( ret )

def ajax_productAutocomplete(request):
  q = request.GET.get('term', '')
  products = Product.objects.filter( name__icontains = q )[:20]
  results = []
  for product in products:
      product_json = {}
      product_json['id'] = product.id
      product_json['label'] = product.name
      product_json['value'] = product.name
      results.append( product_json )
  data = json.dumps( results )
  print "data %s " % data
  return HttpResponse( data )


class ProductForm( forms.Form ):
  family = forms.ModelChoiceField( queryset = Family.objects.all() )
#   subFamily = forms.ModelChoiceField( queryset = SubFamily.objects.all(),
#                      widget = forms.Select( attrs = {'disabled':'disabled'} ) )
  subFamily = forms.ModelChoiceField( queryset = SubFamily.objects.all() )
  products = forms.ModelChoiceField( queryset = Product.objects.all() )

  product = forms.CharField()
  startDay = forms.DateField( initial = datetime.date.today, widget = AdminDateWidget )
  endDay = forms.DateField( initial = datetime.date.today , widget = AdminDateWidget )

def dyn_form( request ):

    form = ProductForm()  # An unbound form

    return render( request, 'comedi/dyn_form.html', {
        'form': form,
    } )

