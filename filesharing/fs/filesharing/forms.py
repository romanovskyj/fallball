__author__ = 'eromanovskyj'

from django import forms

class ResellerChangeForm(forms.Form):

    def __init__(self, resellers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for reseller in resellers:
            self.fields['mark_%d' % reseller.id] = forms.BooleanField(required=False)

class CompanyChangeForm(forms.Form):

    def __init__(self, companies, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for company in companies:
            self.fields['mark_%d' % company.id] = forms.BooleanField(required=False)

class ResellerCreateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    partnerid = forms.CharField()


class CompanyCreateForm(forms.Form):

    def __init__(self, resellerId, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resellerId'] = forms.CharField(widget=forms.HiddenInput(attrs={'value':resellerId}))

    companyname = forms.CharField()