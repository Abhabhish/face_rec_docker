from django.db import models

class FaceData(models.Model):
    file_path   = models.CharField(max_length=255)
    encodings = models.BinaryField()
