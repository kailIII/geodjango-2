from django.db import models
from django.contrib.gis.db import models

class BeerLocs(models.Model):
	lng = models.FloatField()
	lat = models.FloatField()
	bar = models.CharField(max_length=200)
	locs = models.PointField()


class Neighborhoods(models.Model):
    name = models.CharField(max_length=80)
    geom = models.MultiPolygonField()
    objects = models.GeoManager()





