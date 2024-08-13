from __future__ import unicode_literals
from django.db import models, transaction
from authentication.models import User
import uuid
from django.contrib.auth.hashers import make_password
from django.conf import settings
from .error import InsufficientBalance


# Create your models here.

class Wallet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(("balance"), max_digits=100, decimal_places=2, default=0)
    pin = models.IntegerField(max_length=6, default=000000)
    created = models.DateTimeField(auto_now_add=True)
    


    def deposit(self, value):
    
        self.transaction_set.create(
            value=value,
            running_balance=self.balance + value
        )
        self.balance += value
        self.save()


    def withdraw(self, value):
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
        if value > self.current_balance:
            raise InsufficientBalance('This wallet has insufficient balance.')

        self.transaction_set.create(
            value=-value,
            running_balance=self.balance - value
        )
        self.balance -= value
        self.save()

    def transfer(self, wallet, value):
        """Transfers an value to another wallet.

        Uses `deposit` and `withdraw` internally.
        """
        self.withdraw(value)
        wallet.deposit(value)


class Transaction(models.Model):
    # The wallet that holds this transaction.
    wallet = models.ForeignKey(Wallet, on_delete=models.SET_NULL, null=True)

    # The value of this transaction.
    value = models.DecimalField(max_digits=100, decimal_places=2)
    # The value of the wallet at the time of this
    # transaction. Useful for displaying transaction
    # history.
    running_balance = models.DecimalField(max_digits=10, decimal_places=2)

    # The date/time of the creation of this transaction.
    created_at = models.DateTimeField(auto_now_add=True)