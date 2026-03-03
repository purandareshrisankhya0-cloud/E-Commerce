from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True)
    # optionally you could store the Firestore document id if you use both systems
    firestore_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

