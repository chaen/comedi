from django.shortcuts import render
from django import forms
from comedi.models import Client, Period, Order
from django.contrib.admin.widgets import AdminDateWidget
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView




class OrderSearchForm( forms.Form ):
#   clients = forms.ModelChoiceField( queryset = Client.objects.all(), empty_label = "-------", required = False )
  clientChoices = [( 0, '----------' )] + [( c.id, c.complete_name ) for c in Client.objects.all()]
  clients = forms.ChoiceField( choices = clientChoices, required = False )
  client = forms.CharField( required = False )
  startDate = forms.DateField( widget = AdminDateWidget, required = False )
  endDate = forms.DateField( widget = AdminDateWidget, required = False )

  periodChoices = [( 0, '----------' )] + [( p.id, p.name ) for p in Period.objects.all()]
  period = forms.ChoiceField( periodChoices, required = False )

  def is_valid( self ):
    # run the parent validation first
    valid = super( OrderSearchForm, self ).is_valid()

    # we're done now if not valid
    if not valid:
      return valid
    if self.cleaned_data['client'] or self.cleaned_data['startDate']\
      or self.cleaned_data['endDate'] or self.cleaned_data['period'] :
      return True
    else:
      return False

def orderSearch_view( request ):
    form = OrderSearchForm()  # An unbound form
#     request.session['order_form'] = dict()
    request.session.pop( 'order_form', None )
    return render( request, 'comedi/order/order_search.html', {
        'form': form,
    } )



class orderList_view( ListView ):
  model = Order
  template_name = "comedi/order/order_list.html"
  paginate_by = 10
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
        self.request.session.setdefault( 'order_form', {} )['startDate'] = startDate.strftime( "%Y-%m-%d" )

      endDate = form.cleaned_data['endDate']
      if endDate:
        self.request.session.setdefault( 'order_form', {} )['endDate'] = endDate.strftime( "%Y-%m-%d" )

      period = form.cleaned_data['period']
      if period and period != u'0':
        print "yes, period..."
        self.request.session.setdefault( 'order_form', {} )['period'] = period
    return super( orderList_view, self ).get( request, *args, **kwargs )

  def get_queryset( self ):
    searchFilters = self.request.session.get( 'order_form', {} )
    print "searchFilters %s" % searchFilters
    queryset = Order.objects.all()
    if 'client' in  searchFilters:
      queryset = queryset.filter( client__complete_name__iexact = searchFilters.get( 'client' ) )
    if 'startDate' in  searchFilters:
      queryset = queryset.filter( pickup_date__gte = searchFilters.get( 'startDate' ) )
    if 'endDate' in  searchFilters:
      queryset = queryset.filter( pickup_date__lte = searchFilters.get( 'endDate' ) )
    if 'period' in  searchFilters:
        queryset = queryset.filter( period__id__iexact = searchFilters.get( 'period' ) )
    return queryset


  def post( self, request, *args, **kwargs ):
    self.form = OrderSearchForm( request.POST )  # A form bound to the POST data
    return self.get( request, *args, **kwargs )




class orderDetail_view(DetailView):
  model = Order
  template_name = 'comedi/order/order_detail.html'
