from django.db import models

def name_file(instance, filename):
    return '/'.join(['badge', str(instance.label), filename])

class CoinDetails(models.Model):
    category=models.CharField(max_length=100, null=True, blank=True) 
    label=models.CharField(max_length=100, null=True, blank=True) 
    description=models.CharField(max_length=500, null=True, blank=True)
    Image = models.ImageField(upload_to=name_file, null=True, blank=True)
    coinvalue=models.IntegerField(null=True,blank=True)
    entryrange=models.CharField(max_length=100,null=True,blank=True)
    coinvalue1=models.IntegerField(null=True,blank=True)
    entryrange1=models.CharField(max_length=100,null=True,blank=True)
    coinvalue2=models.IntegerField(null=True,blank=True)
    entryrange2=models.CharField(max_length=100,null=True,blank=True)
    coming_soon=models.BooleanField()

    class Meta:
        db_table = 'coin_detail'

    def __str__(self):
        return self.label