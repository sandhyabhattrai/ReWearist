from django.db import models
from django.contrib.auth.models import User
from wearist.models import Products
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Products,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class Order(models.Model):
    PAYMENT = (
        ('Cash on Delivery','Cash on Delivery'),
        ('Esewa','Esewa'),
        ('Khalti','Khalti')
    )
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(null=True)
    status = models.CharField(max_length=100,default='Pending...')
    payment_method = models.CharField(max_length=100,choices=PAYMENT,default='Cash on Delivery')
    payment_status = models.BooleanField(default=False)
    contact_no = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def create_profile_for_user(user):
    UserProfile.objects.get_or_create(user=user)