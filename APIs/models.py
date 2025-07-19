from django.db import models
from rest_framework import serializers


# Create your models here.
class newcustomerdatamodel(models.Model):
    customer_id  = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    age = models.IntegerField()
    phone_number = models.BigIntegerField()
    monthly_income = models.IntegerField()
    approved_limit = models.IntegerField()

    def __str__(self):
        return self.first_name + " " + self.last_name


# Create your models here. 
class loandata(models.Model):
    id  = models.AutoField(primary_key=True)
    Customer_id = models.ForeignKey(newcustomerdatamodel,to_field="customer_id",db_column="Customer_id",  on_delete=models.CASCADE)
    Loan_ID = models.IntegerField()
    Loan_amount = models.IntegerField()
    Tenure = models.IntegerField()
    Interest_rate = models.FloatField()
    EMI = models.IntegerField()
    EMIPOT = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.Customer_id 

