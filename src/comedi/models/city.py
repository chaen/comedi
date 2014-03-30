from django.db import models

class City(models.Model):

  code = models.IntegerField(max_length = 5)
  name = models.CharField(max_length = 50)
  
  def __unicode__(self):
    return "%s (%s)"%(self.name, self.code)
  
  class Meta:
    app_label = 'comedi'