from django.db import models

from city import City

class Client(models.Model):

  first_name = models.CharField(max_length = 50)
  last_name = models.CharField(max_length = 50)
  nickname = models.CharField(max_length = 50, blank = True)
  phone = models.CharField(max_length = 15)
  cellphone = models.CharField(max_length = 15, blank = True)
  email = models.EmailField(max_length = 50, blank = True)
  comment = models.TextField(max_length = 200, blank = True)
  star = models.IntegerField(choices = [ (i, i) for i in range(1,6)], default = 1)
  address = models.CharField(max_length = 50)
  city = models.ForeignKey(City)
  
  def __unicode__(self):
    return "%s %s"%(self.first_name, self.last_name)
  
    
  class Meta:
    app_label = 'comedi'


class Seller( models.Model ):
  name = models.CharField( max_length = 50 )

  def __unicode__( self ):
    return "%s" % ( self.name )


  class Meta:
    app_label = 'comedi'
