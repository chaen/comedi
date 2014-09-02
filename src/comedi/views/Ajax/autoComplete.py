from comedi.models import Client, Product, Period, SubFamily
import json
from django.http import HttpResponse
from django.db.models import Q

def ajax_clientAutocomplete( request ):
  q = request.GET.get( 'term', '' )
  clients = Client.objects.filter( Q( first_name__icontains = q ) | Q( last_name__icontains = q ) )[:20]
  results = []
  for client in clients:
      client_json = {}
      client_json['id'] = client.id
      client_json['label'] = client.complete_name
      client_json['value'] = client.complete_name
      results.append( client_json )
  data = json.dumps( results )
  return HttpResponse( data )

def ajax_productAutocomplete( request ):
  q = request.GET.get( 'term', '' )
  products = Product.objects.filter( name__icontains = q ) [:20]
  results = []
  for product in products:
      product_json = {}
      product_json['id'] = product.id
      product_json['label'] = product.name
      product_json['value'] = product.name
      results.append( product_json )
  sortedResults = sorted(results, key = lambda x: x['label'])
  data = json.dumps( sortedResults )
  return HttpResponse( data )



def ajax_periodAutocomplete( request ):
  q = request.GET.get( 'term', '' )
  periods = Period.objects.filter( name__icontains = q ) [:20]
  results = []
  for period in periods:
      period_json = {}
      period_json['id'] = period.id
      period_json['label'] = period.name
      period_json['value'] = period.name
      results.append( period_json )
  data = json.dumps( sorted( results, key = lambda x: x['label'] ) )
  return HttpResponse( data )


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
  products = sorted( products, key = lambda x: x[1] )
  try:
    ret = json.dumps( products )
  except Exception, e:
    print e
  return HttpResponse( ret )
