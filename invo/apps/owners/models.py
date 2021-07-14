from django.contrib.sites.models import Site
from django.db import models


class SharedSite(models.Model):
    sites = models.ManyToManyField(Site)

    class Meta:
        abstract = True


class SingularSite(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class Meta:
        abstract = True
