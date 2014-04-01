from django.db import models

class Family(models.Model):

  name = models.CharField(max_length = 50)

  def __unicode__( self ):
    return "%s" % ( self.name )

  class Meta:
    app_label = 'comedi'

class SubFamily(models.Model):
  
  name = models.CharField(max_length = 50)
  family = models.ForeignKey(Family)
  
  def __unicode__( self ):
    return "%s" % ( self.name )

  class Meta:
    app_label = 'comedi'

class Tva(models.Model):

  name = models.CharField(max_length = 50)
  rate = models.FloatField()

  def __unicode__( self ):
    return "%s (%s %%)" % ( self.name, self.rate )

  class Meta:
    app_label = 'comedi'

class Unit(models.Model):
  
  name = models.CharField(max_length = 50)
  
  def __unicode__( self ):
    return "%s" % ( self.name )

  class Meta:
    app_label = 'comedi'



class Product(models.Model):

  name = models.CharField( max_length = 50, unique = True )
  code = models.IntegerField( unique = True )
  price = models.FloatField()
  subFamily = models.ForeignKey(SubFamily)
  ttc = models.BooleanField(default = True)
  tva = models.ForeignKey(Tva)
  prod_unit = models.ForeignKey(Unit, related_name = 'prod_unit')
  sell_unit = models.ForeignKey(Unit, related_name = 'sell_unit')
  locked = models.BooleanField(default = False)
  
  def __unicode__( self ):
    return "%s" % ( self.name )

  class Meta:
    app_label = 'comedi'

class UnitConversion( models.Model ):
  
  start_unit = models.ForeignKey(Unit, related_name = 'start_unit')
  end_unit = models.ForeignKey(Unit, related_name = 'end_unit')
  rate = models.FloatField(default = 1)
  product = models.ForeignKey(Product)

  def __unicode__( self ):
    return "%s: %s -> %s" % ( self.product, self.start_unit, self.end_unit )

  class Meta:
    app_label = 'comedi'
