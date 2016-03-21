__author__ = 'eromanovskyj'

from django import forms

class ResellerChangeForm(forms.Form):

    def __init__(self, resellers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for reseller in resellers:
            self.fields['mark_%d' % reseller.id] = forms.BooleanField(required=False)

class ResellerCreateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    partnerid = forms.CharField()