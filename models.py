from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Offer(models.Model):
    bname = models.CharField(max_length=150)
    description = models.TextField()
    bimage = models.ImageField(upload_to='media')
    bdate = models.DateField(default=datetime.datetime.now() ,blank = True , null=True)
    offer_code = models.CharField(max_length = 150)
    is_percentage = models.BooleanField(default= False)
    rate = models.IntegerField()
    closed = models.BooleanField(default = False)

   # def __str__(self):
    #    return self.banner_name

class Slot(models.Model):
    slot_name = models.CharField(max_length=150)
    time = models.TimeField()
    end_time = models.TimeField()
    cancel = models.BooleanField(default = False)
    price = models.IntegerField()

    def __str__(self):
        return self.slot_name

# class Transaction(models.Model):
#     tdate = models.DateField()
#     userId = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.IntegerField()
#     balance = models.IntegerField()
#     partialpayment = models.BooleanField()
#     iscancelled = models.BooleanField()
#     slot_name = models.ForeignKey(Slot, on_delete=models.CASCADE)
#     points = models.IntegerField()

# class Coin(models.Model):
#     userid = models.ForeignKey(User, on_delete=models.CASCADE)
#     referenceid = models.CharField(max_length=150)
#     n_share = models.IntegerField()
#     n_coins = models.IntegerField()

# class Coinsref(models.Model):
#     userid = models.ForeignKey(User, on_delete=models.CASCADE)
#     logined = models.BooleanField()
#     referenceid = models.ForeignKey(Coin, on_delete=models.CASCADE)

class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    mobile = models.BigIntegerField()
    mailid = models.CharField(max_length=300)
    address = models.CharField(max_length=250)
    ref_code = models.CharField(max_length=100)
    coin_balance = models.IntegerField(default = 0)

class Referrals(models.Model):
    parent = models.ForeignKey(User, on_delete = models.CASCADE)
    child = models.CharField(max_length = 250)
    coins_earned = models.IntegerField()



class Gallery(models.Model):
    image = models.ImageField(upload_to='media')
    date = models.DateField()


class Settings(models.Model):
    bookingstatus = models.BooleanField()
    coinsref = models.IntegerField()
    one_coin = models.IntegerField()
    maxcoin = models.IntegerField()
    coinsper_ref = models.IntegerField()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete = models.CASCADE, related_name = 'slot')
    date = models.DateField()
    amount = models.IntegerField()
    coins_used = models.IntegerField()
    offer_applied = models.CharField(max_length=150, null= True, blank= True)
    offer_amount = models.IntegerField(default= 0)
    total_amount = models.IntegerField()

class Feedback(models.Model):
    username = models.CharField(max_length=150)
    feedback = models.TextField()



