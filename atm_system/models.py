from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # username=models.CharField(max_length=100)
    # password=models.CharField(max_length=100)
    balance=models.FloatField(default=0.0)
    # email=models.EmailField()

def __str__(self):
    return self.username



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Withdraw', 'Withdraw'),
        ('Deposit', 'Deposit'),
        ('Transfer', 'Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₹{self.amount}"
