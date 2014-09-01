from django.db import models
from django.utils.translation import ugettext as _


from person import Client, Seller
from period import Period
from product import Product, Unit

class DepositMode( models.Model ):
  name = models.CharField( max_length = 50 )

  class Meta:
    app_label = 'comedi'
    verbose_name = _( 'deposit mode' )


class UsualComment( models.Model ):

  comment = models.CharField( max_length = 200 )

  def __unicode__( self ):
    return "%s" % ( self.comment )

  class Meta:
    app_label = 'comedi'
    verbose_name = _( 'usual comment' )
    verbose_name_plural = _( 'usual comments' )



class Order( models.Model ):

  code = models.CharField( max_length = 10, verbose_name = _( 'code' ) )
  client = models.ForeignKey( Client, verbose_name = _( 'client' ) )
  comment = models.TextField( max_length = 200, blank = True, verbose_name = _( 'comment' ) )
  deposit = models.ForeignKey( DepositMode, blank = True, null = True, verbose_name = _( 'deposit' ) )
  order_date = models.DateField(verbose_name = _( 'order date' ))
  pickup_date = models.DateField( verbose_name = _( 'pickup date' ))
  seller = models.ForeignKey( Seller, verbose_name = _( 'seller' ) )
  period = models.ForeignKey( Period , verbose_name = _( 'period' ) )
  valid = models.BooleanField( default = True, verbose_name = _( 'valid' ) )


  def __unicode__( self ):
    return "%s (%s - %s)" % ( self.code, self.client, self.pickup_date )

  class Meta:
    app_label = 'comedi'
    verbose_name = _( 'order' )
    verbose_name_plural = _( 'orders' )

class OrderItem( models.Model ):

  product = models.ForeignKey( Product, verbose_name = _( 'product' ) )
  unit = models.ForeignKey( Unit, verbose_name = _( 'unit' )  )
  quantity = models.FloatField( verbose_name = _( 'quantity' ) )
  usualComment = models.ForeignKey( UsualComment, blank = True, null = True, verbose_name = _( 'usual comment' ) )
  extraComment = models.TextField( blank = True, verbose_name = _( 'extra comment' ) )
  order = models.ForeignKey( Order, verbose_name = _( 'order' ) )
  prepared = models.BooleanField( default = False, verbose_name = _( 'prepared' ) )
  modified = models.BooleanField( default = False, verbose_name = _( 'modified' ) )
  ordered = models.BooleanField( default = False, verbose_name = _( 'ordered' ) )

  class Meta:
    app_label = 'comedi'
    verbose_name = _( 'item' )
    verbose_name_plural = _( 'items' )


  def __unicode__( self ):
    return "%s %s %s" % ( self.product, self.quantity, self.unit )
