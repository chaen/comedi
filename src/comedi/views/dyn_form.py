from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import ModelForm
from django import forms
from comedi.models import Product, Family, SubFamily
from django.shortcuts import render_to_response


import json


# <script>
#     $("#id_subFamily").change(function() {
#       var subfamily = $(this).val();
#       alert( subfamily.concat(" Handler for .change() called.")  );
#     });
# </script>


# <script>
# $("#id_family").change(function() {
#     var family = $(this).val();
#     $.getJSON("{% url 'list_subfamilies' %}", { family: family }, function(id_subFamily) {
#         var id_subFamily_select = $("#id_subFamily");
#     });
# });
# </script>

def list_subFamilies( request ):
  subFamilies = dict( ( sf.id , sf.name ) for sf in SubFamily.objects.filter( family__pk = request.GET["family"] ) )
  try:
    ret = json.dumps( subFamilies )
  except Exception, e:
    print e
  print "coucou!! %s %s %s" % ( request.GET["family"], subFamilies, ret )
  return HttpResponse( ret )

class ProductForm(ModelForm):
  family = forms.ModelChoiceField( queryset = Family.objects.all() )
  class Meta:
    model = Product

def dyn_form( request ):

    form = ProductForm()  # An unbound form

    return render( request, 'comedi/dyn_form.html', {
        'form': form,
    } )

