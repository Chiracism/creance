from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import DepositForm, WithdrawalForm

from django.db.models import F

# …

# queryset2 = queryset2.annotate(
#     amount_restant=F('amount_arrete') - F('amount_percu')
# )

@login_required()
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        deposit.user.account.balance += deposit.amount
        # deposit.user.account.balance += deposit.amount_arrete
        # deposit.user.account.amount_arrete -= deposit.amount_percu
        # deposit.user.account.amount_restant = deposit.amount_arrete
        deposit.user.account.amount_restant += deposit.amount_restant
        deposit.user.account.save()
        messages.success(request, 'Vous avez déposé {} $.'
                        .format(deposit.amount_restant))
        # messages.success(request, 'le solde restant est de {} $.'
        #                 .format(deposit.calculate_balance))
        return redirect("home")

    @register.filter
    def subtract(value, arg):
        return value - arg

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


@login_required()
def withdrawal_view(request):
    form = WithdrawalForm(request.POST or None, user=request.user)

    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        withdrawal.save()
        # subtracts users withdrawal from balance.
        withdrawal.user.account.amount_restant -= withdrawal.amount_restant
        withdrawal.user.account.save()
        # withdrawal.user.account.balance -= withdrawal.amount
        # withdrawal.user.account.save()

        messages.success(
            # request, 'Vous avez retiré {} $.'.format(withdrawal.amount),
            request, 'Vous avez retiré {} $.'.format(withdrawal.amount_restant)
        )
        return redirect("home")

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "transactions/form.html", context)
