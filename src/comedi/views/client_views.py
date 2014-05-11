from comedi.models import Client
from django.views.generic.detail import DetailView


class clientDetail_view( DetailView ):
  model = Client
  template_name = 'comedi/client/client_detail.html'
