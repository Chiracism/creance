from django import forms

from .models import Deposit, Withdrawal


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["amount"]
        fields = ["libelle"]
        fields = ["reference"]
        fields = ["amount_arrete"]
        fields = ["amount_percu"]
        fields = ["amount_restant"]

        def clean_amount(self):
            amount_restant = self.cleaned_data['amount_restant']
            amount_percu = self.cleaned_data['amount_percu']
            amount_arrete = self.cleaned_data['amount_arrete']

            if self.user.account.amount_arrete < amount_percu:
                raise forms.ValidationError(
                    'Vous ne pouvez pas déposer plus que le montant arreté.'
                )

            return amount_restant

        def subtract(value, arg):
            return value - arg

    # @register.filter
    def subtract(value, arg):
        return value - arg

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["libelle"]
        fields = ["reference"]
        fields = ["amount"]
        fields = ["amount_restant"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount_restant(self):
        # amount = self.cleaned_data['amount']
        amount_restant = self.cleaned_data['amount_restant']

        if self.user.account.amount_restant < amount_restant:
            raise forms.ValidationError(
                'Vous ne pouvez pas retirer plus que votre solde.'
            )

        return amount_restant

    def clean_amount_restant(self):
        # amount = self.cleaned_data['amount']
        amount_restant = self.cleaned_data['amount_restant']

        if self.user.account.amount_restant < amount_restant:
            raise forms.ValidationError(
                'Vous ne pouvez pas retirer plus que votre solde.'
            )

        return amount_restant

    # def clean_amount(self):
    #     amount = self.cleaned_data['amount']
    #     amount_restant = self.cleaned_data['amount_restant']

    #     if self.user.account.balance < amount:
    #         raise forms.ValidationError(
    #             'You Can Not Withdraw More Than You Balance.'
    #         )

    #     return amount
