from django.db import models
from django.contrib.auth.hashers import check_password, make_password



class Category(models.Model):
    name = models.CharField(max_length=255)
    is_income = models.BooleanField()
    
    def __str__(self):
        return self.name
    

    
class Transaction(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    ammount = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ammount} - {self.category.name}"
    


class Currency(models.Model):
    code = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code} ({self.symbol})"



class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.email



class Wallet(models.Model):
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    transactions = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wallets"
    )

    def __str__(self):
        return f"Wallet {self.user.email} [{self.currency.code if self.currency else "No Currency"}]"

    
    
    
    
    
    
    
    
    