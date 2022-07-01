from decimal import Decimal
from optparse import Values
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


User = settings.AUTH_USER_MODEL


class Deposit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='deposits',
        on_delete=models.CASCADE,
    )
    TYPE_DOCUMENT = (
        ("A", "Arriéré Salaire"),
        ("C", "Collation"),
        ("R", "Remboursement"),
        ("O", "Ordre de Mission"),
    )
    libelle = models.CharField(max_length=1, choices=TYPE_DOCUMENT)
    reference = models.CharField(max_length=255)
    amount_arrete = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    amount_percu = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )

    def calculate_balance(self):
        amount_restant = (self.amount_arrete - self.amount_percu)
        return amount_restant

    amount_restant = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user)


class Withdrawal(models.Model):
    user = models.ForeignKey(
        User,
        related_name='withdrawals',
        on_delete=models.CASCADE,
    )
    TYPE_DOCUMENT = (
        ("A", "Arriéré Salaire"),
        ("C", "Collation"),
        ("R", "Remboursement"),
        ("O", "Ordre de Mission"),
    )
    libelle = models.CharField(max_length=1, choices=TYPE_DOCUMENT)
    reference = models.CharField(max_length=255)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    amount_restant = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        default=0,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Interest(models.Model):
    user = models.ForeignKey(
        User,
        related_name='interests',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
