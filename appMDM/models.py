from django.db import models

# Create your models here.

class Doc(models.Model):
    def __str__(self):
        return f'{self.strClasse}'
    numDoc = models.PositiveBigIntegerField('numero',unique=True)
    txtDoc = models.TextField('documento', blank=True)
    strClasse = models.CharField('classe', max_length=100, blank=True)
