from django.db import models


class Car(models.Model):
    price = models.FloatField(db_index=True)


class Truck(models.Model):
    size = models.IntegerField(db_index=True)
