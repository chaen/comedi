from django.shortcuts import render
from django import forms
from comedi.models import Client, Period, Order, Product
from django.contrib.admin.widgets import AdminDateWidget
from django.views.generic.list import ListView
from utilities.pdfGeneration import PDFResponseMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.translation import gettext_lazy as _



class FarSearchForm( forms.Form ):
#   clients = forms.ModelChoiceField( queryset = Client.objects.all(), empty_label = "-------", required = False )
  productChoices = [( 0, '----------' )] + [( p.id, p.name ) for p in Product.objects.all()]
  products = forms.ChoiceField( choices = productChoices, required = False )
  product = forms.CharField()
  startDate = forms.DateField( widget = AdminDateWidget, required = False )
  endDate = forms.DateField( widget = AdminDateWidget, required = False )


@login_required
def farSearch_view( request ):
    form = FarSearchForm()  # An unbound form
    request.session.pop( 'far_form', None )
    return render( request, 'comedi/far/far_search.html', {
        'form': form,
    } )


class FarObj:

  def __init__( self, order_id, order_code, client_id, client_name, quantity, comment, pickup_date, prepared, ordered ):
    self.order_id = order_id
    self.order_code = order_code
    self.client_id = client_id
    self.client_name = client_name
    self.quantity = quantity
    self.comment = comment
    self.pickup_date = pickup_date
    self.prepared = prepared
    self.ordered = ordered


class farList_view( PDFResponseMixin, ListView ):
#   model = Order
  template_name = "comedi/far/far_list.html"
  paginate_by = 10
  context_object_name = "far_list"
  form = None
  
  pdf_title = None
  pdf_pagesize = 'landscape'
  pdf_table_title = ["N", _( "Client" ), _( "Quantity" ), _( "Comment" ), _( "Pickup date" )]
  pdf_table_attribute = ["order_code", "client_name", "quantity", "comment", "pickup_date"]


  def get( self, request, *args, **kwargs ):
    if self.form:
      form = self.form
    else:
      form = FarSearchForm( request.GET )  # A form bound to the POST data

    if form.is_valid():

      product = form.cleaned_data['product']
      if product:
        self.request.session.setdefault( 'far_form', {} )['product'] = product

      startDate = form.cleaned_data['startDate']
      if startDate:
        self.request.session.setdefault( 'far_form', {} )['startDate'] = startDate.strftime( "%Y-%m-%d" )

      endDate = form.cleaned_data['endDate']
      if endDate:
        self.request.session.setdefault( 'far_form', {} )['endDate'] = endDate.strftime( "%Y-%m-%d" )


    else:
      if not 'product' in request.session.get('far_form',{}):
        return render( request, 'comedi/far/far_search.html', {
          'form': form,
          } )

    return super( farList_view, self ).get( request, *args, **kwargs )


  def get_queryset( self ):
    searchFilters = self.request.session.get( 'far_form', {} )
    product = searchFilters['product']
    self.pdf_title = "FAR %s" % product
    orderWithFarProduct = Order.objects.filter( orderitem__product__name = product )

    if 'startDate' in  searchFilters:
      orderWithFarProduct = orderWithFarProduct.filter( pickup_date__gte = searchFilters.get( 'startDate' ) )
    if 'endDate' in  searchFilters:
      orderWithFarProduct = orderWithFarProduct.filter( pickup_date__lte = searchFilters.get( 'endDate' ) )

  
    queryset = []

    for order in orderWithFarProduct:
      order_id = order.id
      order_code = order.code
      client_id = order.client.id
      client_name = order.client.complete_name
      orderItems = order.orderitem_set.filter( product__name = product )
      pickup_date = order.pickup_date
      for item in orderItems:
        quantity = "%s %s"%(item.quantity, item.unit.name)
        comment = "%s %s" % ( item.usualComment.comment if item.usualComment else "", item.extraComment )
        
        queryset.append( FarObj( order_id, order_code, client_id, client_name, quantity, comment, pickup_date, item.prepared, item.ordered ) )

    return queryset
  
  def get_pdf_style_per_line( self, orderedItemList ):
    style = []
    for item in orderedItemList:
      itemStyle = None
      if item.ordered:
        itemStyle = ( 'TEXTCOLOR', 'orange' )
      if item.prepared:
        itemStyle = ( 'TEXTCOLOR', 'blue' )

      style.append( itemStyle )
    return style


  def post( self, request, *args, **kwargs ):
    self.form = FarSearchForm( request.POST )  # A form bound to the POST data
    return self.get( request, *args, **kwargs )

  def get_context_data( self, **kwargs ):
    context = super( farList_view, self ).get_context_data( **kwargs )
    context['far_prod'] = self.request.session.get( 'far_form', {} ).get( 'product' )
    return context




