from django.db import models
from django.urls import path


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    image=models.ImageField(upload_to='drimg/',default='nothing')
    address=models.CharField(max_length=100,default='nothing')
    phone=models.IntegerField(default='1')
    department=models.CharField(max_length=100,default='nothing')
    idnumber=models.IntegerField(default='1')
    id_card=models.ImageField(upload_to='idcard/',default='nothing')
    is_verified = models.BooleanField('Is Verified', default=False)
    def __str__(self):
        return self.name




class Staff(models.Model):
    name = models.CharField(max_length=100)
    email=models.CharField(max_length=50,default='nothing')
    license = models.ImageField(upload_to='license/',default='nothing')
    password =models.CharField(max_length=18,default='nothing')
    image=models.ImageField(upload_to='drimg/',default='nothing')
    address=models.CharField(max_length=100,default='nothing')
    phone=models.IntegerField(default='1')
    status=models.CharField(max_length=20,default='Not Verified')
    is_verified = models.BooleanField('Is Verified', default=False)
    def __str__(self):
        return self.name



class foodmenu(models.Model):
    userid=models.ForeignKey(Staff,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ftype = models.CharField(max_length=500)
    image = models.ImageField(upload_to="vehicles/", blank=True)
    rate=models.IntegerField(null=True)
    status=models.CharField(max_length=20,default="not booked")
    quantity=models.IntegerField(default=10)
    
    
    def __str__(self):
        return self.name

class booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    food=models.ForeignKey(foodmenu, on_delete=models.CASCADE,null=True,blank=True)
    time=models.TimeField(auto_now=True)
    date=models.DateField(auto_now=True)

    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='1')
    cname=models.CharField(max_length=25)
    amount=models.IntegerField()
    cardno=models.IntegerField()
    cvv=models.IntegerField()
    
    
class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(foodmenu)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    checkout_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout by {self.user.name} on {self.checkout_date}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ForeignKey(foodmenu,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.items.name


