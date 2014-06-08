from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
from django import forms

from comedi.models import Period


def statistic( request ):
  return render( request, 'comedi/statistic/statistic_period.html' )
  # return HttpResponse( "Hello, world. You're at the polls index." )

def getTestData( request ):
  tbl = [['a', 'b', 'c', 'd', 'e'], [1, 2, 3, 4, 5]]
  data = json.dumps( tbl )
  return HttpResponse( data )


class StatisticPeriodForm( forms.Form ):
#   clients = forms.ModelChoiceField( queryset = Client.objects.all(), empty_label = "-------", required = False )
  periodChoices = [( p.id, p.name ) for p in Period.objects.all()]
  periods = forms.ChoiceField( periodChoices, required = False )
  initPeriod = periodChoices[0][1] if len( periodChoices ) else ""
  period = forms.CharField( initial = initPeriod )


def statisticPeriod_view( request ):
    form = StatisticPeriodForm()  # An unbound form
#     request.session['order_form'] = dict()
    request.session.pop( 'statistic_period_form', None )
    return render( request, 'comedi/statistic/statistic_period.html', {
        'form': form,
    } )

def statisticShow_view( request ):
  return render( request, 'comedi/statistic/testStat.html' )
  # return HttpResponse( "Hello, world. You're at the polls index." )


def getMostSoldItemsForPeriod( request ):
  periodName = request.GET["periodName"]
  labels = []
  data = []

  perProd = {}
  try:
    period = Period.objects.filter( name__iexact = periodName )[0]
    for order in period.order_set.all():
      for orderItem in order.orderitem_set.all():
        productName = orderItem.product.name
        if productName not in perProd:
          perProd[productName] = 0
        perProd[productName] += 1

    mostSold = sorted( perProd.iteritems(), key = lambda ( k, v ): ( v, k ), reverse = True )[:10]

    for lab, val in mostSold:
      labels.append( lab )
      data.append( val )

  except Exception, e:
    pass

  tbl = [labels, data]
  return HttpResponse( json.dumps( tbl ) )
