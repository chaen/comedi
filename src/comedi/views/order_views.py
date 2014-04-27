from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import ModelForm
from django import forms
from comedi.models import Client, Period, Order
from django.shortcuts import render_to_response
import datetime
from django.contrib.admin.widgets import AdminDateWidget
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
import json




class OrderSearchForm( forms.Form ):
  clients = forms.ModelChoiceField( queryset = Client.objects.all(), empty_label = "-------", required = False )
  client = forms.CharField( required = False )
  startDate = forms.DateField( widget = AdminDateWidget, required = False )
  endDate = forms.DateField( widget = AdminDateWidget, required = False )
  period = forms.ModelChoiceField( queryset = Period.objects.all(), empty_label = "-------", required = False )

def orderSearch_view( request ):

    form = OrderSearchForm()  # An unbound form
    request.session['order_form'] = {}

    return render( request, 'comedi/order/order_search.html', {
        'form': form,
    } )



class orderList_view( ListView ):
  model = Order
  template_name = "comedi/order/order_list.html"
  paginate_by = 1
  context_object_name = "order_list"
  form = None


  def get( self, request, *args, **kwargs ):
    if self.form:
      form = self.form
    else:
      form = OrderSearchForm( request.GET )  # A form bound to the POST data

    if form.is_valid():
      client = form.cleaned_data['client']
      if client:
        self.request.session.setdefault( 'order_form', {} )['client'] = client

      startDate = form.cleaned_data['startDate']
      if startDate:
        self.request.session['order_form']['startDate'] = startDate

      endDate = form.cleaned_data['endDate']
      if endDate:
        self.request.session['order_form']['endDate'] = endDate

      period = form.cleaned_data['period']
      if period:
        self.request.session['order_form']['period'] = period

    return super( orderList_view, self ).get( request, *args, **kwargs )

  def get_queryset( self ):
    searchFilters = self.request.session.get( 'order_form', {} )
    print "searchFilters %s" % searchFilters
    queryset = Order.objects.all()
    if 'client' in  searchFilters:
      queryset = queryset.filter( client__last_name__icontains = searchFilters.get( 'client' ) )
    if 'startDate' in  searchFilters:
      queryset = queryset.filter( order_date__gte = searchFilters.get( 'startDate' ) )
    if 'endDate' in  searchFilters:
      queryset = queryset.filter( order_date__lte = searchFilters.get( 'endDate' ) )
    if 'period' in  searchFilters:
        queryset = queryset.filter( period__exact = searchFilters.get( 'period' ) )
    return queryset


  def post( self, request, *args, **kwargs ):
    self.form = OrderSearchForm( request.POST )  # A form bound to the POST data
    return self.get( request, *args, **kwargs )


class orderDetail_view(DetailView):
  model = Order
  template_name = 'comedi/order/order_detail.html'
