from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from datetime import datetime
from realtors.models import Realtor


class Book(models.Model):
    realtor = models.ForeignKey(
        Realtor, on_delete=models.DO_NOTHING, blank=True, default=None)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=200)
    price = models.IntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    # address = models.CharField(max_length=200)
    # city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # zipcode = models.CharField(max_length=20)
    # bedrooms = models.IntegerField()
    # bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    # garage = models.IntegerField(default=0)
    # sqft = models.IntegerField()
    # lot_size = models.DecimalField(max_digits=5, decimal_places=1)

    def __str__(self):
        return self.title


@receiver(signals.pre_save, sender=Book)
def saveBookToExcel(sender, instance, **kwargs):
    print("Pre Save Is called")


# signals.post_save.connect(receiver=saveBookToExcel, sender=Book)
