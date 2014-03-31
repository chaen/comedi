from django.db import models

class Family(models.Model):

  name = models.CharField(max_length = 50)

  class Meta:
    app_label = 'comedi'

class SubFamily(models.Model):
  
  name = models.CharField(max_length = 50)
  family = models.ForeignKey(Family)
  
  class Meta:
    app_label = 'comedi'

class Tva(models.Model):

  name = models.CharField(max_length = 50)
  rate = models.FloatField()

  class Meta:
    app_label = 'comedi'

class Unit(models.Model):
  
  name = models.CharField(max_length = 50)
  
  class Meta:
    app_label = 'comedi'

class Product(models.Model):

  code = models.IntegerField()
  price = models.FloatField()
  subFamily = models.ForeignKey(SubFamily)
  ttc = models.BooleanField(default = True)
  tva = models.ForeignKey(Tva)
  prod_unit = models.ForeignKey(Unit, related_name = 'prod_unit')
  sell_unit = models.ForeignKey(Unit, related_name = 'sell_unit')
  locked = models.BooleanField(default = False)
  
  class Meta:
    app_label = 'comedi'

class UnitConversion(models.Model):
  from comedi.models.product import Product
  
  
  start_unit = models.ForeignKey(Unit, related_name = 'start_unit')
  end_unit = models.ForeignKey(Unit, related_name = 'end_unit')
  rate = models.FloatField(default = 1)
  product = models.ForeignKey(Product)
  
  class Meta:
    app_label = 'comedi'