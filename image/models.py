from django.db import models

# Create your models here.
class UploadImageModel(models.Model):
    caption = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')
    
    def _str_(self):
        return self.caption