from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    new_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    old_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    discount = models.CharField(max_length=6)
    rating = models.DecimalField(max_digits = 3, decimal_places=2)
    feedback = models.PositiveIntegerField()
    link = models.CharField(max_length=1000)    
    
    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'products'