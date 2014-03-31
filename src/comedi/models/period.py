from django.db import models

class Period(models.Model):

  name = models.CharField(max_length = 50)
  begin_date = models.DateField()
  end_date = models.DateField()
  archived = models.BooleanField(default = False)
  comment = models.TextField(max_length = 200, blank = True)

  def __unicode__(self):
    return "%s (%s - %s)"%(self.name, self.begin_date, self.end_date)

  class Meta:
    app_label = 'comedi'
