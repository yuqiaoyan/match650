# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Algo(models.Model):
    fieldlist = models.CharField(max_length=900)
    boost = models.CharField(max_length=900, blank=True)
    threshold = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = u'algo'

class Professor(models.Model):
    phone = models.CharField(max_length=60, blank=True)
    email = models.CharField(max_length=600, blank=True)
    homepage = models.CharField(max_length=1800, blank=True)
    position = models.CharField(max_length=300, blank=True)
    affiliation = models.CharField(max_length=900, blank=True)
    address = models.CharField(max_length=3000, blank=True)
    phduniv = models.CharField(max_length=900, blank=True)
    phdmajor = models.CharField(max_length=900, blank=True)
    bsuniv = models.CharField(max_length=900, blank=True)
    bio = models.TextField(blank=True)
    pictureurl = models.CharField(max_length=3000, db_column='pictureURL', blank=True) # Field name made lowercase.
    coauthorid = models.TextField(db_column='coauthorID', blank=True) # Field name made lowercase.
    interest = models.CharField(max_length=1500)
    arnetid = models.IntegerField(null=True, db_column='arnetID', blank=True) # Field name made lowercase.
    name = models.CharField(max_length=600)
    class Meta:
        db_table = u'professor'

class Result(models.Model):
    stuinterest = models.CharField(max_length=900, db_column='stuInterest') # Field name made lowercase.
    stuname = models.CharField(max_length=150, db_column='stuName') # Field name made lowercase.
    stuaffiliation = models.CharField(max_length=900, db_column='stuAffiliation', blank=True) # Field name made lowercase.
    date = models.DateTimeField()
    pos1id = models.IntegerField(null=True, db_column='pos1ID', blank=True) # Field name made lowercase.
    pos2id = models.IntegerField(null=True, db_column='pos2ID', blank=True) # Field name made lowercase.
    pos3id = models.IntegerField(null=True, db_column='pos3ID', blank=True) # Field name made lowercase.
    algoid = models.ForeignKey(Algo, db_column='algoID') # Field name made lowercase.
    class Meta:
        db_table = u'result'

