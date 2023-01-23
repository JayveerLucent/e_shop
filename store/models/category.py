from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length= 20)
    
    def __str__(self):
        return self.name
    
    def get_all_categories():
        return Categories.objects.all()