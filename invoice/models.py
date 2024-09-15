from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class BasicData(models.Model):
    salary = models.DecimalField("Salary", max_digits=10, decimal_places=2)
    status = models.CharField("Status", max_length=250)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 


class Billing(models.Model):
    data = models.ForeignKey(BasicData, related_name="dados", on_delete=models.CASCADE)
    month = models.CharField("Month", max_length=250)
    status = models.CharField("Status", max_length=250)
    total = models.DecimalField("Total",max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)


class Itens(models.Model):
    billing = models.ForeignKey(Billing, related_name="cobranca", on_delete=models.CASCADE)
    description = models.CharField("Description", max_length=250)
    value = models.DecimalField("Value",max_digits=10, decimal_places=2)
    required = models.BooleanField("Fixo")
    bank = models.CharField("Bank",max_length=250)

    def __str__(self):
        return str(self.id)


class Investiment(models.Model):
    billing = models.ForeignKey(Billing, related_name="cobranca2", on_delete=models.CASCADE)
    description = models.CharField("Description", max_length=250)
    value = models.DecimalField("Value",max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)