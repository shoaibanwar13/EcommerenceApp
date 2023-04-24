from django.db import models
from django.db import models

class Contact(models.Model):
    name=models.CharField(max_length=200)
    emai=models.EmailField()
    desc=models.CharField(max_length=1000)
    phone=models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=100,default="")
    category=models.CharField(max_length=100,default="")
    subcategory=models.CharField(max_length=100,default="")
    price=models.IntegerField()
    desc=models.CharField(max_length=1009,default="")
    image=models.ImageField(upload_to='images/images')
    
    def __str__(self):
        return self.product_name

class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    iteam_name=models.CharField(max_length=200)
    amount=models.IntegerField()
    name=models.CharField(max_length=50)
    email=models.EmailField()
    address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    zipcode=models.CharField(max_length=200)
    oid=models.CharField(max_length=200)
    payment_status=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Orderupdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField()
    update_desc=models.CharField(max_length=200)
    delivered=models.BooleanField()
    timestamp=models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.update_desc[0:7] + "...."
class Service(models.Model) :
    service_name=models.CharField(max_length=200)
    service_desc=models.TextField()
    
    def __str__(self):
        return self. service_name
         
        
class emailsubcription(models.Model):
    email=models.EmailField()
    
    def __str__(self):
        return self.email
class ReturnProduct(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    pname=models.CharField(max_length=50)
    pid=models.CharField(max_length=50)
    reason=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    zip=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pnumber=models.IntegerField()
    delivered=models.TextField(default="Dot Delivered")
    
    def __str__(self):
        return self.name
    
    
          
    
    
# Create your models here.

# Create your models here.
