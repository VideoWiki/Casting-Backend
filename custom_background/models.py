from django.db import models

# Create your models here.


class background_pictures(models.Model):
    name = models.CharField(max_length=200)
    picture_categories = (
        ('bussiness red', 'Bussiness Red'),
        ('forest green', 'Forest Green'),
        ('grassland green', 'Grassland Green'),
        ('machine grey', 'Machine Grey'),
        ('ocean teal', 'Ocean Teal'),
        ('personal pink', 'Personal Pink'),
        ('river blue', 'River Blue'),
        ('solar yellow', 'Solar Yellow'),
        ('space purple', 'Space Purple'),
        ('sunny orange', 'Sunny Orange'),
    )
    category = models.CharField(max_length=100, choices=picture_categories)
    created = models.DateTimeField(auto_now_add=True)
    high_quality_url = models.URLField()
    low_quality_url = models.URLField()
    credit = models.CharField(max_length=50, blank=True)
    class Meta:
        managed = True
        db_table = 'background_pictures'
    def __str__(self):
        return self.name