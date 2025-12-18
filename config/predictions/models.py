from django.db import models
from django.contrib.auth.models import User


class Predictions(models.Model):
    PREDICTION_CHOICES = (
        ('legitimate','Legitimate'),
        ('phishing','Phishing'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='predictions')
    url = models.URLField(max_length=2048)
    prediction = models.CharField(max_length=20,choices=PREDICTION_CHOICES)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction}"
    
    
