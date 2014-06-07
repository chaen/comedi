from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json



def index( request ):
  return render( request, 'comedi/index.html' )
  # return HttpResponse( "Hello, world. You're at the polls index." )

def getGraphData( request ):
  tbl = [['a', 'b', 'c', 'd', 'e'], [1, 2, 3, 4, 5]]
  data = json.dumps( tbl )
  return HttpResponse( data )

@login_required
def index_loggedIn( request ):
  return HttpResponse( "BIENBUEEEE" )


def logout_view( request ):
    logout( request )
    return HttpResponse( "You're out!" )
