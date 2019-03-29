from .models import Measurement, Variable
from django.shortcuts import render, redirect
from .forms import VariableForm, MeasurementForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import requests

def index(request):
    return render(request, 'index.html')

@login_required
def MeasurementList(request):
    queryset = Measurement.objects.all().order_by('-dateTime')[:10]
    context = {
        'measurement_list': queryset
    }
    return render(request, 'Measurement/measurements.html', context)

def MeasurementCreate(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save()
            measurement.save()
            messages.add_message(request, messages.SUCCESS, 'Measurement create successful')
            return HttpResponseRedirect(reverse('measurementCreate'))
        else:
            print(form.errors)
    else:
        form = MeasurementForm()

    context = {
        'form': form,
    }

    return render(request, 'Measurement/measurementCreate.html', context)

@login_required
def VariableList(request):
    role = getRole(request)
    if role == "Gerencia Campus":
        queryset = Variable.objects.all()
        context = {
            'variable_list': queryset
        }
        return render(request, 'Variable/variables.html', context)
    else:
        return HttpResponse("Unauthorized User")

@login_required
def VariableCreate(request):
    role = getRole(request)
    if role == "Gerencia Campus":
        if request.method == 'POST':
            form = VariableForm(request.POST)
            if form.is_valid():
                measurement = form.save()
                measurement.save()
                messages.add_message(request, messages.SUCCESS, 'Variable create successful')
                return HttpResponseRedirect(reverse('variableCreate'))
            else:
                print(form.errors)
        else:
            form = VariableForm()

        context = {
            'form': form,
        }
        return render(request, 'Variable/variableCreate.html', context)
    else:
        return HttpResponse("Unauthorized User")



def getRole(request):
    user = request.user
    auth0user = user.social_auth.get(provider="auth0")
    accessToken = auth0user.extra_data['access_token']
    url = "https://isis2503-whatevercamps.auth0.com/userinfo"
    headers = {'authorization': 'Bearer ' + accessToken}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()
    role= userinfo['https://isis2503-whatevercamps:auth0:com/role']
    return (role)