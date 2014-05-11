from comedi.models.person import Client
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
