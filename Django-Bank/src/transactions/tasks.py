from __future__ import absolute_import, unicode_literals
from celery.decorators import task

from accounts.models import User
from .models import Interest

@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg


@task(name="count_interest")
def count():
    users = User.objects.filter(account__balance__isnull=False, account__amount_restant__isnull=False)

    if users.exists():
        for user in users:
            balance = user.balance
            amount_arrete = user.amount_arrete
            amount_percu = user.amount_percu
            amount_restant = user.amount_restant 
            # calculates users interest
            amount = (balance * 10) / 100
            Interest.objects.create(user=user, amount=amount)
            # adds users interest to balance.
            user.account.balance += amount
            user.account.amount_arrete += amount_arrete
            user.account.amount_percu += amount_percu
            user.account.amount_restant += amount_restant
            user.account.save()
