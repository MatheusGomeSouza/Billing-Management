from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from invoice.models import BasicData, Billing, Itens, Investiment
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
    full = []
    fix = 0
    var = 0
    inve = 0
    soma_total = 0
    for item in billings_obj:
        billing_id = item.id
        total = 0
        contas = Itens.objects.filter(billing_id=billing_id)
        for conta in contas:
            soma_total += 1
            if conta.required == True:
                fix+=1
            else:
                var+=1
            total += conta.value
        month.append(item.month)
        investimentos = Investiment.objects.filter(billing_id=billing_id)
        if investimentos:
            for inv in investimentos:
                soma_total += 1
                inve+=1
                full.append(int(total)+int(inv.value))
        else:
            full.append(int(total))
       
    perc = [(fix*100)/soma_total,(var*100)/soma_total,(inve*100)/soma_total]
    context = {"basic_obj":basic_obj, "billings":billings_obj,"month":json.dumps(month), "total":json.dumps(full), "perc":json.dumps(perc)}
    # context = RequestContext(request,{"basic_obj":basic_obj})
    return render(request, 'guest/chart.html', context)


def item_form(request, billing_id):
    itens_obj = Itens.objects.filter(billing_id=billing_id)
    investiment = Investiment.objects.filter(billing_id=billing_id)
    context = {"itens":itens_obj,"billing_id":billing_id,"investiment":investiment}
    return render(request,'guest/items.html', context)

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
        obj = Billing(data_id=data_id, month=month, status='Open',total=0)
        obj.save()
    return redirect('/form/')

def itens(request):
    if request.method=='POST':
        billing_id = request.POST['billing']
        description = request.POST['description']
        value = request.POST['value']
        required = request.POST['required']
        bank = request.POST['bank']
        obj = Itens(billing_id=billing_id, description=description, value=value, required=required, bank=bank)
        obj.save()
    return redirect(f'/itens/{billing_id}/')

def investiment(request):
    if request.method=='POST':
        description = request.POST['description']
        billing_id = request.POST['billing']
        value = request.POST['value']
        obj = Investiment(billing_id=billing_id, value=value, description=description)
        obj.save()
    return redirect(f'/itens/{billing_id}/')