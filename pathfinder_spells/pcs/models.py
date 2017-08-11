from django.db import models


class PCClass(models.Model):
    name = models.CharField(max_length=128)
