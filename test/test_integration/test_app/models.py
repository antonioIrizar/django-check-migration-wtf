from django.db import models


class Car(models.Model):
    price = models.FloatField(db_index=True)
