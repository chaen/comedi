from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import ModelForm
from django import forms
from comedi.models import Product, Family, SubFamily
from django.shortcuts import render_to_response
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView

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
  subFamilyObjs = SubFamily.objects.filter( family__pk = request.GET["family"] ) 
  if not subFamilyObjs:
    subFamilyObjs = SubFamily.objects.all()
  subFamilies = dict( ( sf.id , sf.name ) for sf in subFamilyObjs )
#   subFamilies[-1] = "---------"
  try:
    ret = json.dumps( subFamilies )
  except Exception, e:
    print e
  return HttpResponse( ret )

def ajax_getProductNamesFromSubFamily( request ):
  productObjs = Product.objects.filter( subFamily__pk = request.GET["subFamily"] ) 
  if not productObjs:
    productObjs = Product.objects.all()
  products = dict( ( p.id , p.name ) for p in productObjs )
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
  family = forms.ModelChoiceField( queryset = Family.objects.all(), required = False )
#   subFamily = forms.ModelChoiceField( queryset = SubFamily.objects.all(),
#                      widget = forms.Select( attrs = {'disabled':'disabled'} ) )
  subFamily = forms.ModelChoiceField( queryset = SubFamily.objects.all(), required = False )
  products = forms.ModelChoiceField( queryset = Product.objects.all(), empty_label = "-------", required = False )

  product = forms.CharField()
  startDay = forms.DateField( initial = datetime.date.today, widget = AdminDateWidget )
  endDay = forms.DateField( initial = datetime.date.today , widget = AdminDateWidget )

def dyn_form( request ):

    form = ProductForm()  # An unbound form
    request.session.pop( 'dyn_form', None )

    return render( request, 'comedi/dyn_form.html', {
        'form': form,
    } )

def dyn_form_result( request ):

  if request.method == 'POST': # If the form has been submitted...                                                                                                                                                 
    form = ProductForm(request.POST) # A form bound to the POST data                                                                                                                                             
    if form.is_valid(): # All validation rules pass                                                                                                                                                              
      product_name = form.cleaned_data['product']
      print "Product %s"%product_name
      product = get_object_or_404( Product, name = product_name )
      return render( request, 'comedi/dyn_form_result.html', {'product': product} )


class dyn_form_result2( ListView ):
  model = Product
  template_name = "comedi/dyn_form_result2.html"
  paginate_by = 1
  context_object_name = "product_list"
  form = None
#   def get_context_data( self, **kwargs ):
#     context = super( dyn_form_result2, self ).get_context_data( **kwargs )
#     return context

  def get( self, request, *args, **kwargs ):
    if self.form:
      form = self.form
    else:
      form = ProductForm( request.GET )  # A form bound to the POST data

    if form.is_valid():
      productName = form.cleaned_data['product']
#       self.request.session.setdefault( 'dyn_form', {} )['productName'] = productName
      self.request.session.setdefault( 'dyn_form', {} )['productName'] = productName
#       print "AND HERE %s" % self.request.session.get( 'dyn_form', {} ).get( 'productName', None )
      self.productName = productName
    else:
#       self.productName = self.request.session.get( 'dyn_form', {} ).get( 'productName', None )
      self.productName = None
      if self.request.session:
        self.productName = self.request.session.get( 'dyn_form', {} ).get( 'productName', None )

      


    return super( dyn_form_result2, self ).get( request, *args, **kwargs )

  def get_queryset( self ):
#     print "REQUEST %s SESSION %s" % ( self.request.GET, self.request.session )
    print "PRODUCTNAME %s" % self.productName
    if self.productName:
      queryset = Product.objects.filter( name__icontains = self.productName )
    else:
      queryset = []
    return queryset

  def get_context_data( self, **kwargs ):
    context = super( dyn_form_result2, self ).get_context_data( **kwargs )
    print "CONTEXT %s" % context
    return context

  def post( self, request, *args, **kwargs ):
    self.form = ProductForm( request.POST )  # A form bound to the POST data
    return self.get( request, *args, **kwargs )

