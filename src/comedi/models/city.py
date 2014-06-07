from django.db import models
from django.utils.translation import gettext_lazy as _

class City(models.Model):

  code = models.IntegerField( max_length = 5, verbose_name = _( 'zip' ) )
  name = models.CharField( max_length = 50, verbose_name = _( 'name' ) )
  
  def __unicode__(self):
    return "%s (%s)"%(self.name, self.code)
  
  class Meta:
    app_label = 'comedi'
    verbose_name = _( 'city' )
    verbose_name_plural = _( 'cities' )
