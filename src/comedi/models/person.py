from django.db import models
from django.utils.translation import gettext_lazy as _

from city import City

class Client(models.Model):

  first_name = models.CharField( max_length = 50, verbose_name = _( 'first name' ) )
  last_name = models.CharField( max_length = 50, verbose_name = _( 'last name' ) )
  nickname = models.CharField( max_length = 50, blank = True, verbose_name = _( 'nickname' ) )
  complete_name = models.CharField( max_length = 50, editable = False )
  phone = models.CharField( max_length = 15, verbose_name = _( 'phone' ) )
  cellphone = models.CharField( max_length = 15, blank = True, verbose_name = _( 'mobile' ) )
  email = models.EmailField(max_length = 50, blank = True)
  comment = models.TextField( max_length = 200, blank = True, verbose_name = _( 'comment' ) )
  star = models.IntegerField( choices = [ ( i, i ) for i in range( 1, 6 )], default = 1, verbose_name = _( 'star' ) )
  address = models.CharField( max_length = 50, verbose_name = _( 'address' ) )
  city = models.ForeignKey( City, verbose_name = _( 'city' ) )
  
  def __unicode__(self):
    return "%s %s"%(self.first_name, self.last_name)

  def save( self, *args, **kwargs ):
    complete_name = '%s %s' % ( self.first_name, self.last_name )
    self.complete_name = complete_name
    super( Client, self ).save( *args, **kwargs )
    
  class Meta:
    app_label = 'comedi'
    verbose_name = _( 'client' )
    verbose_name_plural = _( 'clients' )


class Seller( models.Model ):
  name = models.CharField( max_length = 50, verbose_name = _( 'name' ) )

  def __unicode__( self ):
    return "%s" % ( self.name )


  class Meta:
    app_label = 'comedi'
    verbose_name = _( 'seller' )
    verbose_name_plural = _( 'sellers' )
