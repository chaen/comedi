from django.db import models
from django.utils.translation import gettext_lazy as _

class Family(models.Model):

  name = models.CharField( max_length = 50, verbose_name = _( 'name' ) )

  def __unicode__( self ):
    return "%s" % ( self.name )

  class Meta:
    app_label = 'comedi'
    verbose_name = 'family'
    verbose_name_plural = 'families'

class SubFamily(models.Model):
  
  name = models.CharField( max_length = 50 , verbose_name = _( 'name' ) )
  family = models.ForeignKey( Family, verbose_name = _( 'family' ) )
  
  def __unicode__( self ):
    return "%s" % ( self.name )

  class Meta:
    app_label = 'comedi'
    verbose_name = 'subFamily'
    verbose_name_plural = 'subFamilies'

class Tva(models.Model):

  name = models.CharField(max_length = 50, verbose_name = _( 'name' ))
  rate = models.FloatField( verbose_name = _( 'rate' ) )

  def __unicode__( self ):
    return "%s (%s %%)" % ( self.name, self.rate )

  class Meta:
    app_label = 'comedi'


class Unit(models.Model):
  
  name = models.CharField( max_length = 50, verbose_name = _( 'name' ) )
  
  def __unicode__( self ):
    return "%s" % ( self.name )

  class Meta:
    app_label = 'comedi'
    verbose_name = 'unit'
    verbose_name_plural = 'units'


class Product(models.Model):

  name = models.CharField( max_length = 50, unique = True , verbose_name = _( 'name' ))
  code = models.IntegerField( unique = True, verbose_name = _( 'code' ) )
  price = models.FloatField( verbose_name = _( 'price' ) )
  subFamily = models.ForeignKey(SubFamily, verbose_name = _( 'subFamily' ))
  ttc = models.BooleanField(default = True)
  tva = models.ForeignKey(Tva)
  prod_unit = models.ForeignKey( Unit, related_name = 'prod_unit', verbose_name = _( 'production unit' ) )
  sell_unit = models.ForeignKey( Unit, related_name = 'sell_unit', verbose_name = _( 'sell unit' ) )
  locked = models.BooleanField( default = False, verbose_name = _( 'locked' ) )
  
  def __unicode__( self ):
    return "%s" % ( self.name )

  class Meta:
    app_label = 'comedi'
    verbose_name = 'product'
    verbose_name_plural = 'products'

class UnitConversion( models.Model ):
  
  start_unit = models.ForeignKey( Unit, related_name = 'start_unit', verbose_name = _( 'start unit' ) )
  end_unit = models.ForeignKey( Unit, related_name = 'end_unit', verbose_name = _( 'end unit' ) )
  rate = models.FloatField( default = 1, verbose_name = _( 'rate' ) )
  product = models.ForeignKey( Product, verbose_name = _( 'product' ) )

  def __unicode__( self ):
    return "%s: %s -> %s" % ( self.product, self.start_unit, self.end_unit )

  class Meta:
    app_label = 'comedi'
    verbose_name = 'unit conversion'
