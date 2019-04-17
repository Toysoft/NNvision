from django.db import models

# Create your models here.

class Config(models.Model):
    dataset = models.CharField(max_length=50, unique=True, blank=True, null=True )
    size = models.SmallIntegerField()
    name = models.CharField(max_length=200, blank=True )
    ratio = models.FloatField(default = 1)
    valid = models.BooleanField(default=False)
    
    def __str__(self):
        return self.dataset

    
class Image(models.Model):
    config = models.ForeignKey(Config, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=False, blank=True, null=True)
    process = models.SmallIntegerField()
    class Meta:
        unique_together = ('config', 'name',)
    
    


    
