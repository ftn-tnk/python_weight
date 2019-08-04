from django.db import models

# Create your models here.
class Weightapp(models.Model):
    use_date = models.DateTimeField('Date & Date')
    weight = models.IntegerField(default=0)
    bodyfat = models.IntegerField(default=0)
    detail = models.CharField(max_length=200)
    category = models.CharField(max_length=10)

    def __str__(self):
        return str(self.use_date) + ' /' + self.detail + ' /' + str(self.weight)
