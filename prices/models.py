from django.db import models
from django.utils import timezone


class Security(models.Model):
    name = models.CharField(max_length=25, unique=True)
    weight = models.FloatField(default=10.0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'security'


class SecurityPrice(models.Model):
    security = models.ForeignKey('Security', on_delete=models.CASCADE)
    price = models.FloatField()
    registered = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.security) + "  " + str(self.price)

    class Meta:
        db_table = 'security_price'
