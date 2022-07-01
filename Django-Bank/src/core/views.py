from django.db.models import Sum
# from django.db.models import Subtract
from django.shortcuts import render

from transactions.models import Deposit, Withdrawal, Interest

from django.db.models import F

# …

# deposit = deposit.annotate(
#     amount_restant=F('amount_arrete') - F('amount_percu')
# )


def home(request):
    if not request.user.is_authenticated:
        return render(request, "core/index.html", {})
    else:
        user = request.user
        deposit = Deposit.objects.filter(user=user)
        deposit_sum = deposit.aggregate(Sum('amount'))['amount__sum']
        # deposit_subtract = deposit.aggregate(Subtract('amount_arrete'))['amount__sub']
        deposit_arrete = deposit.aggregate(Sum('amount_arrete'))['amount_arrete__sum']
        deposit_rest = deposit.aggregate(Sum('amount_restant'))['amount_restant__sum']
        withdrawal = Withdrawal.objects.filter(user=user)
        withdrawal_sum = withdrawal.aggregate(Sum('amount'))['amount__sum']
        withdrawal = Withdrawal.objects.filter(user=user)
        withdrawal_rest =  withdrawal.aggregate(Sum('amount_restant'))['amount_restant__sum']
        interest = Interest.objects.filter(user=user)
        interest_sum = interest.aggregate(Sum('amount'))['amount__sum']

        context = {
                    "user": user,
                    "deposit": deposit,
                    "deposit_sum": deposit_sum,
                    "deposit_arrete": deposit_arrete,
                    "deposit_rest": deposit_rest,
                    "withdrawal": withdrawal,
                    "withdrawal_sum": withdrawal_sum,
                    "withdrawal_rest": withdrawal_rest,
                    "interest": interest,
                    "interest_sum": interest_sum,
                }

        return render(request, "core/transactions.html", context)


def about(request):
    return render(request, "core/about.html", {})
