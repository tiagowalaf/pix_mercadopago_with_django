from django.db import models

class Product(models.Model):
    nome = models.CharField(max_length=244, blank=True, null=True)
    preco = models.IntegerField()