from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from invoice.models import BasicData, Billing, Itens

# Create your views here.

@csrf_protect
def index(request):
    return render(request,'guest/index.html')

def form(request):
    basic_obj = BasicData.objects.get(user=request.user.id)
    billings_obj = Billing.objects.filter(data=basic_obj.id)
    context = {"basic_obj":basic_obj, "billings":billings_obj}
    # context = RequestContext(request,{"basic_obj":basic_obj})
    return render(request, 'guest/forms.html', context)

def item_form(request, billing_id):
    itens_obj = Itens.objects.filter(billing_id=billing_id)
    context = {"itens":itens_obj,"billing_id":billing_id}
    return render(request,'guest/items.html', context)

def basic(request):
    if request.method=='POST':
        salary = request.POST['Salary']
        user_id = request.POST['user_id']
        obj = BasicData(salary=salary, user_id=user_id, status='Open')
        obj.save()
    return render(request,'guest/forms.html')

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