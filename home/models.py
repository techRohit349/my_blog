from django.db import models

# Model for user query related data
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=13)
    gmail = models.CharField(max_length=150)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True , blank=True)
    
    def __str__(self):
        return "Message from " + self.name +" - " + self.gmail
