from rest_framework import serializers
from .models import newcustomerdatamodel, loandata
import random

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = newcustomerdatamodel
        fields = '__all__'


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = loandata
        fields = '__all__'



class RegisterSerializer(serializers.ModelSerializer):
    approved_limit = serializers.IntegerField(read_only=True)  # ✅ Mark it read-only

    class Meta:
        model = newcustomerdatamodel
        fields = ['first_name', 'last_name', 'age', 'phone_number', 'monthly_income', 'approved_limit']

    def create(self, validated_data):
        customer_id = newcustomerdatamodel.objects.count() + 1
        approved_limit = 36 * validated_data['monthly_income']
        return newcustomerdatamodel.objects.create(
            customer_id=customer_id,
            approved_limit=approved_limit,
            **validated_data
        )

class NewLoanEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.IntegerField()
    tenure = serializers.IntegerField()
    interest_rate = serializers.FloatField()
    corrected_interest_rate = serializers.FloatField(read_only=True)  # Calculated only, not required in input
    approval = serializers.BooleanField(read_only=True)  # Calculated only, not required in input


class NewLoanSerializer(serializers.ModelSerializer):
    Loan_ID = random.randint(1000, 9999)  # Generate a random Loan ID
    customer_id = serializers.IntegerField()
    loan_amount = serializers.IntegerField()
    interest_rate = serializers.FloatField()
    tenure = serializers.IntegerField()
    approval = serializers.BooleanField(read_only=True)  # Calculated only, not required in input
    
    class Meta:
        model = loandata
        fields = ['customer_id', 'loan_amount', 'interest_rate', 'tenure', 'approval', 'Loan_ID']