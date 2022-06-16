from django import forms

from .models import ContractorRelease
from cash.models import ProjectBankAccount, ProjectCashBook, InstallmentPaymentOrder


class ContractRegisterForm(forms.Form):
    project = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'project'}))
    task = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'task'}))
    order_group = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'order_group'}))
    type = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'type'}))
    key_unit = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'key_unit'}))
    house_unit = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'house_unit'}), required=False)
    back_url = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'back_url'}), required=False)

    # Contractor Model
    name = forms.CharField(max_length=10, label='계약자명')
    birth_date = forms.DateField(label='생년월일', required=False)
    GENDER_CHOICES = (('M', '남자'), ('F', '여자'))
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES, required=False, label='성별')
    is_registed = forms.BooleanField(label='인가등록 여부', required=False)
    reservation_date = forms.DateField(label='청약일자', required=False)
    contract_date = forms.DateField(label='계약일자', required=False)
    note = forms.CharField(widget=forms.Textarea, required=False, label='비고')
    # ContractorAddress Model
    id_zipcode = forms.CharField(max_length=5, label='우편번호', required=False)
    id_address1 = forms.CharField(max_length=50, label='주민등록 주소', required=False)
    id_address2 = forms.CharField(max_length=30, label='상세주소', required=False)
    id_address3 = forms.CharField(max_length=30, label='참고항목', required=False)
    dm_zipcode = forms.CharField(max_length=5, label='우편번호', required=False)
    dm_address1 = forms.CharField(max_length=50, label='우편송부 주소', required=False)
    dm_address2 = forms.CharField(max_length=30, label='상세주소', required=False)
    dm_address3 = forms.CharField(max_length=30, label='참고항목', required=False)
    # ContractorContact Model
    cell_phone = forms.CharField(max_length=13, label='휴대전화')
    home_phone = forms.CharField(max_length=13, required=False, label='집 전화')
    other_phone = forms.CharField(max_length=13, required=False, label='기타 전화')
    email = forms.EmailField(required=False, label='이메일')


class ContractorReleaseForm(forms.ModelForm):
    class Meta:
        model = ContractorRelease
        fields = '__all__'
        widgets = {
            'project': forms.HiddenInput(), 'contractor': forms.HiddenInput(),
            'status': forms.HiddenInput(), 'user': forms.HiddenInput()
        }


class ContractPaymentForm(forms.ModelForm):
    class Meta:
        model = ProjectCashBook
        fields = ('deal_date', 'income', 'bank_account', 'trader', 'installment_order')

    def __init__(self, project, *args, **kwargs):
        super(ContractPaymentForm, self).__init__(*args, **kwargs)
        self.fields['bank_account'].queryset = ProjectBankAccount.objects.filter(project=project)
        self.fields['bank_account'].empty_label = '납부계좌선택'
        self.fields['installment_order'].queryset = InstallmentPaymentOrder.objects.filter(project=project,
                                                                                           pay_code__lte='4')
        self.fields['installment_order'].empty_label = '납부회차선택'
