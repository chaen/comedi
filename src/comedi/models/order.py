from django.db import models

from person import Client, Seller
from period import Period
from product import Product, Unit

class DepositMode( models.Model ):
  name = models.CharField( max_length = 50 )

  class Meta:
    app_label = 'comedi'


class UsualComment( models.Model ):

  comment = models.CharField( max_length = 200 )

  class Meta:
    app_label = 'comedi'



class Order( models.Model ):

  code = models.CharField( max_length = 10 )
  client = models.ForeignKey( Client )
  comment = models.TextField( max_length = 200, blank = True )
  deposit = models.ForeignKey( DepositMode, blank = True, null = True )
  order_date = models.DateField()
  pickup_date = models.DateField()
  seller = models.ForeignKey( Seller )
  period = models.ForeignKey( Period )
  valid = models.BooleanField( default = True )
  prepared = models.BooleanField( default = False )
  modified = models.BooleanField( default = False )

  def __unicode__( self ):
    return "%s (%s - %s)" % ( self.code, self.client, self.pickup_date )

  class Meta:
    app_label = 'comedi'

class OrderItem( models.Model ):

  product = models.ForeignKey( Product )
  unit = models.ForeignKey( Unit )
  quantity = models.FloatField()
  usualComment = models.ForeignKey( UsualComment, blank = True, null = True )
  extraComment = models.TextField( blank = True )
  order = models.ForeignKey( Order )

  class Meta:
    app_label = 'comedi'

  def __unicode__( self ):
    return "%s %s %s" % ( self.product, self.quantity, self.unit )
