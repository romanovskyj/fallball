from rest_framework import viewsets
from filesharing.serializers import ResellerSerializer, CompanySerializer
from filesharing.models import Reseller, Company
from django.shortcuts import render, get_object_or_404, redirect
from filesharing.forms import ResellerChangeForm, ResellerCreateForm
from .auxiliary import marked_elements

class ResellerViewSet(viewsets.ModelViewSet):
    queryset = Reseller.objects.all()
    serializer_class = ResellerSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

def resellers(request):

    resellers = Reseller.objects.all()

    if request.method == 'POST':
        collected_form = ResellerChangeForm(data=request.POST,resellers=resellers)

        if collected_form.is_valid():
            form_data = collected_form.cleaned_data
            chosen_reseller_ids = marked_elements(form_data)

            for r_id in chosen_reseller_ids:
                reseller = get_object_or_404(Reseller,pk=r_id)
                reseller.delete()

    return render(request, 'ui/resellers.html', {'resellers': resellers})

def resellerCreate(request):

    if request.method == 'POST':

        # get data that user filled
        collected_form = ResellerCreateForm(data=request.POST)

        if collected_form.is_valid():

            # get data from form
            form_data = collected_form.cleaned_data

            reseller = Reseller(partnerid=form_data['partnerid'])
            reseller.save()

        return redirect('/ui/resellers')

    form = ResellerCreateForm()

    return render(request, 'ui/newreseller.html', {'form': form})

def reseller(request):
    pass

def addCompany(request):
    pass

def deleteCompany(request):
    pass

def deleteReseller(request):
    pass