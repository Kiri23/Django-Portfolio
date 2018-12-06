from django.db import models
from django.db.models import signals
from django.dispatch import receiver

from datetime import datetime

class Excel(models.Model):
    date_modified_past = models.DateTimeField(blank=True, null = True)
    old_fileStr = models.TextField(blank = True, null = True)

    # def __str__(self):
    #     return self.title


@receiver(signals.pre_save, sender=Excel)
def saveBookToExcel(sender, instance, **kwargs):
    print("Pre Save of excel is called")


# signals.post_save.connect(receiver=saveBookToExcel, sender=Book)
