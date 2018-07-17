from django.db import models

# Create your models here.

class Record(models.Model):
	rowid = models.IntegerField(primary_key=True)
	title = models.CharField(max_length=200, blank=True)
	short_description = models.CharField(max_length=500, blank=True)
	long_description = models.CharField(max_length=1500, blank=True)
	sdg_code = models.CharField(max_length=10)

	def __repr__(self):
		return "Record {}: {}".format(self.rowid, self.title)

	def __str__(self):
		return "{}".format(self.title)

