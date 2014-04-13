from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def index( request ):
    return HttpResponse( "Hello, world. You're at the polls index." )

@login_required
def index_loggedIn( request ):
  return HttpResponse( "BIENBUEEEE" )


def logout_view( request ):
    logout( request )
    return HttpResponse( "You're out!" )
