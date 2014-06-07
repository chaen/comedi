from django.db import models
from django.utils.translation import gettext_lazy as _

class Period(models.Model):

  name = models.CharField( max_length = 50, verbose_name = _( 'name' ) )
  begin_date = models.DateField( verbose_name = _( 'begin date' ) )
  end_date = models.DateField( verbose_name = _( 'end date' ) )
  archived = models.BooleanField( default = False, verbose_name = _( 'archived' ) )
  comment = models.TextField( max_length = 200, blank = True, verbose_name = _( 'comment' ) )
  prefix = models.CharField( max_length = 10, blank = True , verbose_name = _( 'prefix' ) )

  def __unicode__(self):
    return "%s (%s - %s)"%(self.name, self.begin_date, self.end_date)

  class Meta:
    app_label = 'comedi'
    verbose_name = _( 'period' )
    verbose_name_plural = _( 'periods' )
