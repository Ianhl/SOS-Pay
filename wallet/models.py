from __future__ import unicode_literals
from django.db import models, transaction
from authentication.models import User
import uuid
from django.contrib.auth.hashers import make_password
from django.conf import settings

from tuckshop.models import Order
from .error import InsufficientBalance
import random
import string
from django.utils import timezone


# Create your models here.

class Wallet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(("balance"), max_digits=100, decimal_places=2, default=0)
    pin = models.CharField(max_length=20)
    created = models.DateTimeField(default=timezone.now)
    private_code = models.CharField(max_length=20, unique=True)
    is_shopowner = models.BooleanField(default=False)
    
    
    def create_wallet(self, user):
        wallet = self.model(user=user)
        
        user.save(using=self._db)


    def save(self, *args, **kwargs):
        if not self.private_code:
            self.private_code = self.generate_private_code()
        super().save(*args, **kwargs)
        
    def generate_private_code(self):
        length = 12
        characters = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            if not Wallet.objects.filter(private_code=code).exists():
                return code    
        
    
    # def generate_private_code(self):
    #     # Generate a unique private code
    #     return str(uuid.uuid4().hex[:12].upper())  # Example: 8e3a8b4b4c6e

    def deposit(self, value, sender):
    
        self.transaction_set.create(
            value=value,
            running_balance=self.balance + value,
            transaction_from= sender,
        )
        self.balance += value
        self.save()


    def withdraw(self, value, sender):
        """Withdraw's a value from the wallet.

        Also creates a new transaction with the withdraw
        value.

        Should the withdrawn amount is greater than the
        balance this wallet currently has, it raises an
        :mod:`InsufficientBalance` error. This exception
        inherits from :mod:`django.db.IntegrityError`. So
        that it automatically rolls-back during a
        transaction lifecycle.
        """
        if int(value) > int(self.balance):
            raise InsufficientBalance('This wallet has insufficient balance.')

        self.transaction_set.create(
            value=-value,
            running_balance=self.balance - value, 
            transaction_from= sender,
        )
        self.balance -= value
        self.save()

    def transfer(self, wallet, value, sender):
        """Transfers an value to another wallet.

        Uses `deposit` and `withdraw` internally.
        """
        self.withdraw(value, sender)
        wallet.deposit(value, sender)


class Transaction(models.Model):
    # The wallet that holds this transaction.
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    # The value of this transaction.
    value = models.DecimalField(max_digits=100, decimal_places=2)
    # The value of the wallet at the time of this
    # transaction.
    # uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    transaction_from = models.CharField(max_length=100, default="")
    running_balance = models.DecimalField(max_digits=10, decimal_places=2)
    # The date/time of the creation of this transaction.
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    email_otp = models.CharField(max_length=6, null=True, blank=True)



