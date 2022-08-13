from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Products(models.Model):   
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('myapp:products')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    desc = models.CharField(max_length=100)
    image = models.ImageField(blank=True, upload_to='images', default='404.png')

class orderDetail(models.Model):
    customer_username = models.CharField(max_length=30)
    product = models.ForeignKey(to='Products', on_delete=models.PROTECT) # protects the field even if the actual field is deleted
    amount = models.IntegerField()
    checkout_session_id = models.CharField(max_length=200) 
    payment_intent = models.CharField(max_length=200, null=True)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True) # adds current dateNtime automatically
    updated_on = models.DateTimeField(auto_now_add=True)
