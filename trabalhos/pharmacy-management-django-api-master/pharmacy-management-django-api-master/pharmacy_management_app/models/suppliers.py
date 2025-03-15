from django.db import models

class Suppliers(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


