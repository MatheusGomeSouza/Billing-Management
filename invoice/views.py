from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from invoice.models import BasicData, Billing, Itens

# Create your views here.

@csrf_protect
def index(request):
    return render(request,'guest/index.html')

def form(request):
    return render(request,'guest/forms.html')

def basic(request):
    if request.method=='POST':
        salary = request.POST['Salary']
        user_id = request.POST['user_id']
        obj = BasicData(salary=salary, user_id=user_id, status='Open')
        obj.save()
    return render(request,'guest/forms.html')

def billing(request):
    if request.method=='POST':
        data = request.POST['data_id']
        month = request.POST['month']
        obj = Billing(data=data, month=month, status='Open',total=0)
        obj.save()
    return render(request,'guest/forms.html')

def itens(request):
    if request.method=='POST':
        billing = request.POST['billing']
        description = request.POST['description']
        value = request.POST['value']
        required = request.POST['required']
        bank = request.POST['bank']
        obj = Itens(billing=billing, description=description, value=value, required=required, bank=bank)
        obj.save()
    return render(request,'guest/forms.html')