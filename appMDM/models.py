from django.db import models

# Create your models here.

class Doc(models.Model):
    def __str__(self):
        return f'{self.strClasse}'
    txtDoc = models.TextField('document', blank=True)
    strClasse = models.CharField('classe', max_length=100, blank=True)
