from django.db import models


class MotorBike(models.Model):
    price = models.FloatField(db_index=True)
