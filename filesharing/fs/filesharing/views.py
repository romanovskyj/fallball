from rest_framework import viewsets
from filesharing.serializers import ResellerSerializer, CompanySerializer
from filesharing.models import Reseller, Company
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from filesharing.forms import ResellerChangeForm, ResellerCreateForm, CompanyChangeForm, CompanyCreateForm
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
        collected_form = ResellerChangeForm(data=request.POST, resellers=resellers)

        if collected_form.is_valid():
            form_data = collected_form.cleaned_data
            chosen_reseller_ids = marked_elements(form_data)

            for r_id in chosen_reseller_ids:
                reseller = get_object_or_404(Reseller, pk=r_id)
                reseller.delete()

        # to avoid deleted objects presentation
        resellers = Reseller.objects.all()

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


def reseller(request, reseller_id):
    reseller = get_object_or_404(Reseller, pk=reseller_id)
    companies = get_list_or_404(Company, resellerid=reseller)

    if request.method == 'POST':
        collected_form = CompanyChangeForm(data=request.POST, companies=companies)

        if collected_form.is_valid():
            form_data = collected_form.cleaned_data
            chosen_company_ids = marked_elements(form_data)

            for c_id in chosen_company_ids:
                company = get_object_or_404(Company, pk=c_id)
                company.delete()

        # to avoid deleted objects presentation
        companies = get_list_or_404(Company, resellerid=reseller)

    return render(request, 'ui/reseller.html', {'reseller': reseller, 'companies': companies})


def companyCreate(request, reseller_id):
    if request.method == 'POST':
        # get data that user filled
        collected_form = CompanyCreateForm(data=request.POST,resellerId = reseller_id)

        if collected_form.is_valid():
            # get data from form
            form_data = collected_form.cleaned_data

            company = Company(companyname=form_data['companyname'], resellerid = form_data['resellerId'])
            company.save()

        return redirect('/ui/resellers/' + reseller_id + '/')


    form = CompanyCreateForm(resellerId = reseller_id)

    return render(request, 'ui/newcompany.html', {'form': form, 'resellerId': reseller_id})


def deleteCompany(request):
    pass


def deleteReseller(request):
    pass
