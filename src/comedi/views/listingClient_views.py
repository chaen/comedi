from django.shortcuts import render
from django import forms
from comedi.models import Client, Period, Order, Product
from django.contrib.admin.widgets import AdminDateWidget
from django.views.generic.list import ListView
from utilities.pdfGeneration import PDFResponseMixin




class ListingClientSearchForm( forms.Form ):
  startDate = forms.DateField( widget = AdminDateWidget )
  endDate = forms.DateField( widget = AdminDateWidget )


def listingClientSearch_view( request ):
    form = ListingClientSearchForm()  # An unbound form
    request.session.pop( 'listingClient_form', None )
    return render( request, 'comedi/listingClient/listingClient_search.html', {
        'form': form,
    } )


class ListingClientObj:

  def __init__( self, order_id, order_code, client_id, client_name, nbOfItems ):
    self.order_id = order_id
    self.order_code = order_code
    self.client_id = client_id
    self.client_name = client_name
    self.nbOfItems = nbOfItems





class listingClientList_view( PDFResponseMixin, ListView ):
#   model = Order
  template_name = "comedi/listingClient/listingClient_list.html"
  paginate_by = 10
  context_object_name = "listingClient_list"
  form = None
  
  pdf_title = None
  pdf_table_title = ["N", "Client name", "Items"]
  pdf_table_attribute = ["order_code", "client_name", "nbOfItems"]


  def get( self, request, *args, **kwargs ):
    if self.form:
      form = self.form
    else:
      form = ListingClientSearchForm( request.GET )  # A form bound to the POST data

    if form.is_valid():

      startDate = form.cleaned_data['startDate']
      if startDate:
        self.request.session.setdefault( 'listingClient_form', {} )['startDate'] = startDate.strftime( "%Y-%m-%d" )

      endDate = form.cleaned_data['endDate']
      if endDate:
        self.request.session.setdefault( 'listingClient_form', {} )['endDate'] = endDate.strftime( "%Y-%m-%d" )


    else:
      if not 'startDate' in request.session.get( 'listingClient_form', {} ):
        return render( request, 'comedi/listingClient/listingClient_search.html', {
          'form': form,
          } )

    return super( listingClientList_view, self ).get( request, *args, **kwargs )


  def get_queryset( self ):
    searchFilters = self.request.session.get( 'listingClient_form', {} )

    startDate = searchFilters.get( 'startDate' )
    endDate = searchFilters.get( 'endDate' )
    listingClient = Order.objects.filter( pickup_date__gte = startDate )\
                          .filter( pickup_date__lte = endDate )

    self.pdf_title = "Listing Client from %s to %s" % ( startDate, endDate )

  
    queryset = []

    for order in listingClient:
      order_id = order.id
      order_code = order.code
      client_id = order.client.id
      client_name = order.client.complete_name
      nbOfItems = order.orderitem_set.count()

      queryset.append( ListingClientObj( order_id, order_code, client_id, client_name, nbOfItems ) )

    return queryset


  def post( self, request, *args, **kwargs ):
    self.form = ListingClientSearchForm( request.POST )  # A form bound to the POST data
    return self.get( request, *args, **kwargs )

  def get_context_data( self, **kwargs ):
    context = super( listingClientList_view, self ).get_context_data( **kwargs )
    context['listingClient_startDate'] = self.request.session.get( 'listingClient_form', {} ).get( 'startDate' )
    context['listingClient_endDate'] = self.request.session.get( 'listingClient_form', {} ).get( 'endDate' )
    return context




