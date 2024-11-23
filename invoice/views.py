from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from invoice.models import BasicData, Billing, Itens, Investiment
from sktime.forecasting.base import ForecastingHorizon
from sktime.forecasting.model_selection import temporal_train_test_split
from sktime.forecasting.theta import ThetaForecaster
from sklearn.preprocessing import LabelEncoder
from sktime.performance_metrics.forecasting import mean_absolute_percentage_error
from sktime.utils.plotting import plot_series
import pandas as pd
import matplotlib.pyplot as plt, mpld3
import numpy as np
import json

# Create your views here.

@csrf_protect
def index(request):
    return render(request,'guest/index.html')

def form(request):
    basic_obj = BasicData.objects.filter(user=request.user.id)
    basic_obj = basic_obj[0] if basic_obj else basic_obj
    billings_obj = Billing.objects.filter(data=basic_obj.id) if basic_obj else None
    context = {"basic_obj":basic_obj, "billings":billings_obj}
    # context = RequestContext(request,{"basic_obj":basic_obj})
    return render(request, 'guest/forms.html', context)

def basic_data(request):
    basic_obj = BasicData.objects.filter(user=request.user.id)
    basic_obj = basic_obj[0] if basic_obj else basic_obj
    billings_obj = Billing.objects.filter(data=basic_obj.id) if basic_obj else None
    month = []
    fix_full = []
    var_full = []
    inve_full = []
    full = []
    fix = 0
    var = 0
    inve = 0
    soma_total = 0
    for item in billings_obj:
        billing_id = item.id
        total = 0
        contas = Itens.objects.filter(billing_id=billing_id)
        fix_sum_conta=0
        var_sum_conta=0
        inv_sum_conta=0
        for conta in contas:
            soma_total += 1
            if conta.required == True:
                fix+=1
                fix_sum_conta+=int(conta.value)
            else:
                var+=1
                var_sum_conta+=int(conta.value)
            total += conta.value
        month.append(item.month)
        investimentos = Investiment.objects.filter(billing_id=billing_id)
        if investimentos:
            total_inv_bill = 0
            for inv in investimentos:
                soma_total += 1
                inve+=1
                inv_sum_conta+=int(inv.value)
                total_inv_bill+=int(inv.value)
            full.append(int(total)+total_inv_bill)
        else:
            full.append(int(total))
        fix_full.append(fix_sum_conta)
        var_full.append(var_sum_conta)
        inve_full.append(inv_sum_conta)


    obj_df = zip(month, full)
    df = pd.DataFrame(obj_df, columns=["month", "full"])

    if df["full"].dtype == 'object':  # Se for string ou categoria
        encoder = LabelEncoder()
        df["full"] = encoder.fit_transform(df["full"])

    y_train, y_test = temporal_train_test_split(df["full"], train_size=0.8)
    fh = ForecastingHorizon(y_test.index, is_relative=False)
    forecaster = ThetaForecaster(sp=4)
    forecaster.fit(y_train)

    y_pred = forecaster.predict(fh)

    mean_absolute_percentage_error(y_test, y_pred)

    fig, ax  = plot_series(df["full"], y_pred)

    g = mpld3.fig_to_html(fig)


    perc = [round(((fix*100)/soma_total),2),round(((var*100)/soma_total),2),round(((inve*100)/soma_total),2)]
    context = {"basic_obj":basic_obj, "billings":billings_obj,"month":json.dumps(month), "total":json.dumps(full), "perc":json.dumps(perc),
               "fix_full":json.dumps(fix_full),"inve_full":json.dumps(inve_full),"var_full":json.dumps(var_full), 'g': g}
    return render(request, 'guest/chart.html', context)

def billing_view(request):
    basic_obj = BasicData.objects.filter(user=request.user.id)
    basic_obj = basic_obj[0] if basic_obj else basic_obj
    context = {}
    # context = RequestContext(request,{"basic_obj":basic_obj})
    return render(request, 'guest/billing.html', context)


def item_form(request, billing_id):
    itens_obj = Itens.objects.filter(billing_id=billing_id)
    investiment = Investiment.objects.filter(billing_id=billing_id)
    billing_obj = Billing.objects.filter(id=billing_id)
    context = {"itens":itens_obj,"billing_id":billing_id,"investiment":investiment, "month": billing_obj[0].month}
    return render(request,'guest/itens.html', context)

def basic(request):
    if request.method=='POST':
        salary = request.POST['Salary']
        user_id = request.POST['user_id']
        obj = BasicData(salary=salary, user_id=user_id, status='Open')
        obj.save()
    return redirect('/form/')

def billing(request):
    if request.method=='POST':
        data_id = request.POST['data_id']
        month = request.POST['month']
        response = Billing.objects.filter(data_id=data_id, month=month)
        if response:
            return redirect('/form/')
        obj = Billing(data_id=data_id, month=month, status='Open',total=0)
        obj.save()
    return redirect('/form/')

def itens(request):
    if request.method=='POST':
        billing_id = request.POST['billing_id']
        description = request.POST['description']
        value = request.POST['value']
        required = request.POST['required']
        bank = request.POST['bank']
        obj = Itens(billing_id=billing_id, description=description, value=value, required=required, bank=bank)
        obj.save()

        bill_obj = Billing.objects.filter(id=billing_id)
        all_itens = Itens.objects.filter(billing_id=billing_id)
        basic_data = BasicData.objects.filter(id=bill_obj[0].data_id)
        soma=0
        if all_itens:
            for i in all_itens:
                soma+=i.value
        status = 'healthy' if basic_data[0].salary > soma else 'value exceeded'
        bill_obj.update(status=status)
    return redirect(f'/itens/{billing_id}/')

def investiment(request):
    if request.method=='POST':
        description = request.POST['description']
        billing_id = request.POST['billing_id']
        value = request.POST['value']
        obj = Investiment(billing_id=billing_id, value=value, description=description)
        obj.save()
        
        bill_obj = Billing.objects.filter(id=billing_id)
        all_itens = Itens.objects.filter(billing_id=billing_id)
        all_inv = Investiment.objects.filter(billing_id=billing_id)
        basic_data = BasicData.objects.filter(id=bill_obj[0].data_id)
        
        soma=0
        if all_itens:
            for i in all_itens:
                soma+=i.value
        if all_inv:
            for i in all_inv:
                soma+=i.value
        status = 'healthy' if basic_data[0].salary > soma else 'value exceeded'
        bill_obj.update(status=status)
    return redirect(f'/itens/{billing_id}/')